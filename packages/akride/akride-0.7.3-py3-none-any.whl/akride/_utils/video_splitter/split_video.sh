#!/bin/bash
set -e
set -x

tmp_dirs=()


# Cleanup temporary directories for non zero exit codes
cleanup(){
   if [ $? -ne 0 ]; then
      echo "Removing"
      for dir in "${tmp_dirs[@]}"; do
            rm -rf "$dir"
            echo "Removed $dir"
      done
    fi

}

trap cleanup EXIT


chunkSize=$1
samplingRate=$2
video=$3
out_dir_parent_path=$4
metadata_file=$5
tmp_parent_dir=$6

export OP_PATH_PREFIX="partitioner/outputs/o1"
METADATA_FILE_PATH="${metadata_file}"


TEMP_DIR=${tmp_parent_dir}/temp

echo "ChunkSize $1, input SamplingRate $2"

mkdir -p $TEMP_DIR

ffprobe -i "$video" -v quiet || printf '{"fps": -1, "height": -1, "width": -1, "duration": -1, "error": 1}' >> ${METADATA_FILE_PATH}
if [[ -f ${METADATA_FILE_PATH} && "$(stat -c%s ${METADATA_FILE_PATH})" -ne 0 ]]; then
    exit 1;
fi

img_properties=$(ffprobe -v 0 -of json=compact=1 -select_streams V:0 -show_entries stream=avg_frame_rate,height,width,duration "$video" | jq -r .'streams[0]')

echo "${img_properties}" >> "${METADATA_FILE_PATH}"

duration=$(echo $img_properties | jq -r '.duration // -1')
height=$(echo $img_properties | jq -r '.height')
width=$(echo $img_properties | jq -r '.width')
fps=$(echo $img_properties | jq -r '.avg_frame_rate')

fps_numerator=$(echo "$fps" | cut -d/ -f1)
fps_denominator=$(echo "$fps" | cut -d/ -f2)
fps=$((fps_numerator / fps_denominator))
if [[ $((fps_numerator % fps_denominator)) != 0 ]]; then
  fps=$((fps + 1))
fi
echo "video $video properties = $img_properties"

error=1
ffmpeg -i "$video" -v error -r $fps $TEMP_DIR/frame%07d.jpg && error=0
printf '{"fps": %d, "height": %d, "width": %d, "duration": %f, "error": %d}' "${fps}" "${height}" "${width}" "${duration}" "${error}" > ${METADATA_FILE_PATH}

if [[ $error -eq 1 ]]; then
  exit 1;
fi

totalFiles=$(ls $TEMP_DIR | wc -l)
folderName=0000000
# batch size is not calculated on basis of sampling rate because frames are dropped on basis of
# sampling rate later. The number of frames in a token will be calculated by sampling rate.
batchSize=$((chunkSize * fps))

# if sampling_rate is greater than fps then don't consider its values
if (( $(echo "$samplingRate>$fps" | bc -l) || $(echo "$samplingRate<=0" | bc -l) )); then
  samplingRate=$fps
fi
# increment counter value to skip the frames if sampling rate is lower than fps
incrCounter=$(echo "$fps/$samplingRate" | bc -l)
echo "Sampling rate of video $samplingRate increment counter $incrCounter"


for ((partition = 1; partition <= totalFiles; partition = $((partition + batchSize)))); do
  folderName=$(printf "%07d" $((10#$folderName + 1)))

  echo "Creating temp directory!"
  out_dir="$(mktemp -d ${out_dir_parent_path}/tmpdir.XXXXXX)/$OP_PATH_PREFIX/$folderName"
  mkdir -p ${out_dir}

  tmp_dirs+=("$out_dir")

  maxPartitionEnd=$((partition + batchSize - 1))                                # Inclusive
  partitionEnd=$((maxPartitionEnd > totalFiles ? totalFiles : maxPartitionEnd)) # Inclusive
  nextFrameNum=$partition
  # dropping the frame here on basis of increment counter calculated by sampling rate and fps
  for ((num = partition; num <= partitionEnd; num = $(echo "$nextFrameNum/1" | bc))); do
    mv "$TEMP_DIR/frame$(printf "%07d" "$num").jpg" "${out_dir}" &
    nextFrameNum=$(echo "$nextFrameNum+$incrCounter" | bc -l)
  done
  wait
done
echo "Created $folderName chunks for video $video"
