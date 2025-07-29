# Building

This project uses rust so you need to install it:  
brew install rust

Use [uv](https://astral.sh/blog/uv)  
Install using **pip install uv**

```console
cargo build -p libaec --release
cp -rf ../target/release/libaec.dylib src/prx_pyaec/
WHEEL_TAG="py3-none-macosx_11_0_arm64" uv build
```

Publish locally using pip  
**pip install --no-index --find-links=./dist/ prx_pyaec**  
then you can test with:  
**uv run --with prx_pyaec --no-project -- python -c "import prx_pyaec"**  


Publish to PyPi (optional -- you'll need a PyPi account and access token)

```console
export UV_PUBLISH_TOKEN="<your PyPi token here>"
uv publish
```

Installing once published

```console
uv run --with prx_pyaec --refresh-package prx_pyaec --no-project -- python -c "import prx_pyaec"
```
