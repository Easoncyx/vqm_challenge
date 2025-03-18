#!/bin/bash
set -e

# Set the working directory to the script's directory
# script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
script_dir="/tmp"
echo "Install ffmpeg from $script_dir";

# Install necessary packages
apt-get install -qq -y wget xz-utils

# Download and extract ffmpeg static build ffmpeg with libvmaf
wget -q https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n7.1-latest-linux64-gpl-7.1.tar.xz -O "${script_dir}/ffmpeg.tar.xz"
tar -xf "${script_dir}/ffmpeg.tar.xz"  -C "${script_dir}"


# Rename the subfolder to "ffmpeg"
mv "${script_dir}/ffmpeg-n7.1-latest-linux64-gpl-7.1" "${script_dir}/ffmpeg"

# Clean up
rm "${script_dir}/ffmpeg.tar.xz"

# Move the binaries to /usr/local/bin/
mv "${script_dir}/ffmpeg/bin/ffmpeg" /usr/local/bin/
mv "${script_dir}/ffmpeg/bin/ffprobe" /usr/local/bin/
mv "${script_dir}/ffmpeg/bin/ffplay" /usr/local/bin/

# Clean up
rm -r "${script_dir}/ffmpeg"

echo "install ffmpeg successful"

# Add path /usr/local/bin to PATH
echo "export PATH=\"/usr/local/bin:$PATH\"" >> ~/.bashrc
source ~/.bashrc
