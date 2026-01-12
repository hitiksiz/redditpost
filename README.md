<h1>Reddit Python SVG post script</h1> 
  
  <img  src="https://raw.githubusercontent.com/hitiksiz/redditpost/main/cover_page-reddit_svg.png" align="center" width="500" height="300">

<p>
A focused utility within <strong>redditpost</strong> that handles uploading
<strong>SVG images</strong> into Reddit-compatible formats.
</p>

<p>
Reddit does <strong>not</strong> allow direct <code>.svg</code> uploads due to security
and format constraints. This module exists to bridge that gap by sanitizing,
converting, and preparing SVG assets for automated Reddit posting workflows.
</p>

<hr/>

<h2>What this module does</h2>

<ul>
  <li>
    <strong>SVG sanitization</strong><br/>
    Removes unsafe elements (scripts, external refs, embedded payloads).
  </li>
  <li>
    <strong>Format conversion</strong><br/>
    Converts SVGs into Reddit-acceptable raster formats such as PNG.
  </li>
  <li>
    <strong>Clean integration</strong><br/>
    Designed to plug directly into Reddit automation pipelines.
  </li>
</ul>

<hr/>

<h2>Who this is for</h2>

<p>Use this module if you:</p>

<ul>
  <li>Generate Reddit post images programmatically</li>
  <li>Design content in SVG but need Reddit-safe uploads</li>
  <li>Want SVG handling isolated from posting logic</li>
</ul>

<hr/>

<h2>Installation</h2>

<pre><code>git clone https://github.com/hitiksiz/redditpost.git
cd redditpost/redditpost/svg_upload
</code></pre>

<p>Install dependencies (will update the repo soon for more):</p>

<pre><code>pip install -r requirements.txt
</code></pre>

<hr/>

<h2>Basic usage</h2>

<pre><code>from svg_upload import svg_processor

svg = svg_processor.load("design.svg")
clean_svg = svg_processor.sanitize(svg)
png_path = svg_processor.convert_to_png(
    clean_svg,
    output="ready_for_reddit.png"
)
</code></pre>

<p>
After conversion, the output image can be passed directly to your Reddit
upload logic.
</p>

<hr/>

<h2>Example API</h2>

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>load(path)</code></td>
      <td>Loads an SVG file from disk</td>
    </tr>
    <tr>
      <td><code>sanitize(svg)</code></td>
      <td>Removes unsafe or unsupported SVG content</td>
    </tr>
    <tr>
      <td><code>convert_to_png(svg, output)</code></td>
      <td>Rasterizes the SVG into a PNG file</td>
    </tr>
  </tbody>
</table>

<p>
<em>Adjust function names if your implementation differs.</em>
</p>

<hr/>

<h2>Security notes</h2>

<ul>
  <li>Never trust raw SVG input from unknown sources.</li>
  <li>Always sanitize before conversion or upload.</li>
  <li>SVGs can contain scripts, links, and hidden payloads.</li>
</ul>

<hr/>

<h2>Why this exists</h2>

<p>
Reddit’s media pipeline does not support SVG uploads. This module enforces
safe, predictable conversion so SVG-based design workflows can still be used
in automated Reddit posting systems.
</p>

<hr/>

<h2>Contributing</h2>

<ol>
  <li>Create a feature branch</li>
  <li>Make changes</li>
  <li>Open a pull request</li>
</ol>

<hr/>

<h2><a href="https://github.com/hitiksiz/redditpost/blob/main/LICENSE">LICENSE</a> </h2>
