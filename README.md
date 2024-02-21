Python scripts to perform some tasks using FFmpeg.

### `encode-video.py`

Creates mkv file from H.265 encoded video and copies of other elementary streams from the source file.
If you specify a directory in the `--input` option, then all files in the specified directory are processed.

**Usage:**
```
encode-video [-h] [-i INPUT] [-o OUTPUT] [--preset PRESET] [--crf CRF] [--scale WIDTH:HEIGHT] [--tune TUNE]
```

**Options:**

<dl>

<dt>
<code>-h</code>, <code>--help</code>
</dt>
<dd>
Show help message and exit.
</dd>
  
<dt>
<code>-i INPUT</code>, <code>--input INPUT</code>
</dt>
<dd>
Input directory or file.<br/> 
Default: <samp>C:/videoconv/input/</samp>.
</dd>

<dt>
<code>-o OUTPUT</code>, <code>--output OUTPUT</code>
</dt>
<dd>
Output directory.<br/>
Default: <samp>C:/videoconv/output/</samp>.
</dd>

<dt>
<code>--preset PRESET</code>
</dt>
<dd>
The preset determines compression efficiency and therefore affects encoding speed.<br/>
Available options: <code>ultrafast</code>, <code>superfast</code>, <code>veryfast</code>, <code>faster</code>, 
<code>fast</code>, <code>medium</code>, <code>slow</code>, <code>slower</code>, <code>veryslow</code>,
<code>placebo</code>.<br/>
Default: <code>slow</code>.
</dd>

<dt>
<code>--crf CRF</code>
</dt>
<dd>
Constant rate factor (the lower CRF, the higher the video quality).<br/>
Default: <code>22</code>.
</dd>

<dt>
<code>--scale WIDTH:HEIGHT</code>
</dt>
<dd>
Resolution parameters of the output video. They are set in the format <samp>width:height</samp> 
(for example, <samp>1920:1080</samp>).
Any of these parameters can be set as <samp>-1</samp> for automatic calculation
(for example, <samp>1920:-1</samp>).<br/>
If this option is not specified, the resolution does not change.<br/>
Default: None.
</dd>

<dt>
<code>--tune TUNE</code>
</dt>
<dd>
Settings based upon the specifics of your input. By default, it is disabled.<br/>
Available options: <code>film</code>, <code>animation</code>, <code>grain</code>, <code>stillimage</code>, 
<code>fastdecode</code>, <code>zerolatency</code>, <code>psnr</code>, <code>ssim</code>.<br/>
Default: None.
</dd>

</dl>
