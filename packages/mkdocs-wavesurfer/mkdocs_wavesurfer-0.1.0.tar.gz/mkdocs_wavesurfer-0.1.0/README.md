# mkdocs-wavesurfer

This is a plugin for [mkdocs](https://www.mkdocs.org/) that adds a waveform display for `<audio>` elements using [wavesurfer.js](https://wavesurfer.xyz/).

This plugin only works when [mkdocs-audiotag](https://github.com/aeskildsen/mkdocs-audiotag) is also installed and enabled.

## Quick start

### Install the plugin

```shell
pip install mkdocs-wavesurfer
```

### Enable the plugin in mkdocs.yml

```yaml
plugins:
  - mkdocs-audiotag # required
  - mkdocs-wavesurfer
```

### Embed an audio file in markdown source

As described on the [mkdocs-audiotag readme](https://github.com/aeskildsen/mkdocs-audiotag).

```markdown
![audio/ogg](my-audio-file.ogg)
```

The waveform will be shown below the audio element's controls.

## Configuration

You can tweak how *wavesurfer.js* displays the waveform using a range of configuration options. See the [wavesurfer.js documentation](https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferOptions) and the very nice [visual examples](https://wavesurfer.xyz/examples/?all-options.js) for a full description.

Add your options under the `mkdocs-wavesurfer` plugin in your `mkdocs.yml`.

```yaml
plugins:
  - mkdocs-audiotag
  - mkdocs-wavesurfer:
      height: 200
      wave_color: "#0fcb2bff"
      progress_color: rgb(0, 100, 0)
      cursor_color: red
      cursor_width: 10
      bar_width: 5
      bar_gap: 2
```

![Waveform canvas generated with the configuration shown above](./waveform-wavesurfer.png)

Note:

- **Defaults:** You only need to specify the options you want to override, as others will use default values.
- **Colors:** Can be specified as in CSS using hex values, rgb(), or color names, as shown in the example above.
- **Case:** We use snake case in `mkdocs.yml` for consistency, as opposed to the wavesurfer.js docs which use javascript and camel case.

### Use with mkdocs-material

The plugin can adapt to the color set by [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) for a visually coherent style.

```yaml
plugins:
  - mkdocs-audiotag
  - mkdocs-wavesurfer:
      use_mkdocs-material_color: true
```

When this is enabled, the options `wave_color` and `progress_color` are overwritten, and the plugin will log a warning if they are present in `mkdocs.yml`.

### Autopopulated options

Please note that the following wavesurfer options are populated automatically by the plugin and cannot be specified in the config:

- `media_controls`
- `media`
- `url`
- `container`

If you would like to remove the browser's default media controls, you can do so by configuring [mkdocs-audiotag](https://github.com/aeskildsen/mkdocs-audiotag):

```yaml
plugins:
  - mkdocs-audiotag:
      controls: false
  - mkdocs-wavesurfer
```

### Default config values

Below are the default configuration values:

```yaml
plugins:
  - mkdocs-wavesurfer:
      height: 128
      width: "100%"
      split_channels: false
      normalize: false
      wave_color: "#ff4e00"
      progress_color: "#dd5e98"
      cursor_color: "#ddd5e9"
      cursor_width: 2
      bar_width: null
      bar_gap: null
      bar_radius: null
      bar_height: null
      bar_align: ""
      min_px_per_sec: 1
      fill_parent: true
      autoplay: false
      interact: true
      drag_to_seek: false
      hide_scrollbar: false
      audio_rate: 1.0
      auto_scroll: true
      auto_center: true
      sample_rate: 8000
      use_mkdocs_material_color: false
```

## License

This plugin is licensed under the MIT license.

Beware that [wavesurfer.js is licensed under the BSD-3-Clause license](https://github.com/katspaugh/wavesurfer.js?tab=BSD-3-Clause-1-ov-file).
