Python scripts to perform some tasks using FFmpeg.

### `encode-video.py`

Creates an mkv file from H.265 encoded video and copies of other elementary streams from the source file.

**Usage:**
```
encode-video [-h] [-i INPUT] [-o OUTPUT] [--crf CRF] [--scale SCALE]
```

**Options:**

<dl>
<dt><code>-h</code>, <code>--help</code></dt>
<dd>Show help message and exit</dd>
  
<dt><code>-i INPUT</code>, <code>--input INPUT</code></dt>
<dd>Input directory or file (default: <samp>C:/videoconv/input/</samp>)</dd>

<dt><code>-o OUTPUT</code>, <code>--output OUTPUT</code></dt>
<dd>Output directory (default: <samp>C:/videoconv/output/</samp>)</dd>

<dt><code>--crf CRF</code></dt>
<dd>Constant rate factor (the lower CRF, the higher the video quality) (default: 22)</dd>

<dt><code>--scale SCALE</code></dt>
<dd>Resolution parameters of the output video. They are set in the format <samp>width:height</samp> (for example, <samp>1920:1080</samp>).
Any of these parameters can be set as <samp>-1</samp> for automatic calculation (for example, <samp>1920:-1</samp>).<br/>
If this option is not specified, the resolution does not change. (default: None)</dd>
</dl>
