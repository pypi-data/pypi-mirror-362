#! /bin/zsh

echo "Ensure you are in the prx_pyaec subdirectory. Enter to continue, Ctrl+C to abort"
read

rm -fr ../target
cargo build -p libaec --release
cp -rf ../target/release/libaec.dylib src/prx_pyaec/
WHEEL_TAG="py3-none-macosx_11_0_arm64" uv build

echo ""
echo "If things build correctly and a new version is in the pyproject.toml file you can "
echo "publish to PyPi using the command: "
echo "uv publish"
echo ""
echo "then update your local site-package using the command: "
echo "pip install prx_pyaec==2.0.3 (or whatever is your version "
echo ""
echo "otherwise, you can update your local copy with these commands:"
echo "rm -fr  ~/miniforge3/envs/prx_aec/lib/python3.11/site-packages/prx_pyaec"
echo "rm -fr ~/miniforge3/envs/prx_aec/lib/python3.11/site-packages/prx_pyaec-2.0.2.dist-info"
echo "pip install --no-index --find-links=./dist/ prx_pyaec"
echo ""

