import mkdocs
import re
import logging
from bs4 import BeautifulSoup as BS

class WaveConfig(mkdocs.config.base.Config):
    # as per https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferOptions
    height = mkdocs.config.config_options.Type(int, default=128)
    width = mkdocs.config.config_options.Type(int | str, default='100%')
    split_channels = mkdocs.config.config_options.Type(bool, default=False)
    normalize = mkdocs.config.config_options.Type(bool, default=False)
    wave_color = mkdocs.config.config_options.Type(str, default='#ff4e00')
    progress_color = mkdocs.config.config_options.Type(str, default='#dd5e98')
    cursor_color = mkdocs.config.config_options.Type(str, default='#ddd5e9')
    cursor_width = mkdocs.config.config_options.Type(int, default=2)
    bar_width = mkdocs.config.config_options.Type(int | float, default=float('nan'))
    bar_gap = mkdocs.config.config_options.Type(int | float, default=float('nan'))
    bar_radius = mkdocs.config.config_options.Type(int | float, default=float('nan'))
    bar_height = mkdocs.config.config_options.Type(int | float, default=float('nan'))
    bar_align = mkdocs.config.config_options.Choice(['top', 'bottom', ''], default='')
    min_px_per_sec = mkdocs.config.config_options.Type(int, default=1)
    fill_parent = mkdocs.config.config_options.Type(bool, default=True)
    autoplay = mkdocs.config.config_options.Type(bool, default=False)
    interact = mkdocs.config.config_options.Type(bool, default=True)
    drag_to_seek = mkdocs.config.config_options.Type(bool, default=False)
    hide_scrollbar = mkdocs.config.config_options.Type(bool, default=False)
    audio_rate = mkdocs.config.config_options.Type(float, default=1.0)
    auto_scroll = mkdocs.config.config_options.Type(bool, default=True)
    auto_center = mkdocs.config.config_options.Type(bool, default=True)
    sample_rate = mkdocs.config.config_options.Type(int, default=8000)

    use_mkdocs_material_color = mkdocs.config.config_options.Type(bool, default=False)

class Wave(mkdocs.plugins.BasePlugin[WaveConfig]):
    def on_config(self, config):
        logger = logging.getLogger("mkdocs.plugins.mkdocs_wavesurfer")
        
        # Build JS options from config
        js_options = {
            'height': self.config.height,
            'width': f"'{self.config.width}'" if isinstance(self.config.width, str) else self.config.width,
            'splitChannels': str(self.config.split_channels).lower(),
            'normalize': str(self.config.normalize).lower(),
            'waveColor': f"'{self.config.wave_color}'",
            'progressColor': f"'{self.config.progress_color}'",
            'cursorColor': f"'{self.config.cursor_color}'",
            'cursorWidth': self.config.cursor_width,
            'barWidth': 'NaN' if self.config.bar_width != self.config.bar_width else self.config.bar_width,
            'barGap': 'NaN' if self.config.bar_gap != self.config.bar_gap else self.config.bar_gap,
            'barRadius': 'NaN' if self.config.bar_radius != self.config.bar_radius else self.config.bar_radius,
            'barHeight': 'NaN' if self.config.bar_height != self.config.bar_height else self.config.bar_height,
            'barAlign': f"'{self.config.bar_align}'",
            'minPxPerSec': self.config.min_px_per_sec,
            'fillParent': str(self.config.fill_parent).lower(),
            'autoplay': str(self.config.autoplay).lower(),
            'interact': str(self.config.interact).lower(),
            'dragToSeek': str(self.config.drag_to_seek).lower(),
            'hideScrollbar': str(self.config.hide_scrollbar).lower(),
            'audioRate': self.config.audio_rate,
            'autoScroll': str(self.config.auto_scroll).lower(),
            'autoCenter': str(self.config.auto_center).lower(),
            'sampleRate': self.config.sample_rate,
        }
        # Log a warning if user has specified use_mkdocs_material_color AND wave_color or progress_color
        if (
            self.config.use_mkdocs_material_color and (
                self.config.wave_color != '#ff4e00' or
                self.config.progress_color != '#dd5e98'
            )
        ):
            logger.warning(
                "mkdocs-wavesurfer: Both 'use_mkdocs_material_color' is enabled and a custom 'wave_color' or 'progress_color' is set. The color options for waveforms will be overwritten by the Material theme color."
            )
        
        # Build JS config string
        options_str = ',\n  '.join(f"{k}: {v}" for k, v in js_options.items())
        config['ws_config_obj'] = f"const options = {{\n  {options_str}\n}};\n"
        
        return config
    
    def on_post_page(self, output, page, config):
        soup = BS(output, 'html.parser')
        html = output

        # find data on audio elements - container and element ids + source paths
        surfers_data = []
        for div in soup.find_all(class_='audio-container'):
            surfers_data.append((div['id'], div.find('audio')['id'], div.find('source')['src']))
        
        if len(surfers_data) > 0:
            js = config['ws_config_obj']
            js += "\nconst surfers = []\n"
            if self.config.use_mkdocs_material_color:
                js += """
function getThemeColor() {
    const metaTag = document.querySelector('meta[name="theme-color"]')
    return metaTag ? metaTag.getAttribute('content') : '#2196f3' // fallback
}
function darkenColor(hex, amount = 0.4) {
    const num = parseInt(hex.slice(1), 16)
    const r = Math.floor((num >> 16) * (1 - amount))
    const g = Math.floor(((num >> 8) & 0x00FF) * (1 - amount))
    const b = Math.floor((num & 0x0000FF) * (1 - amount))
    return `rgb(${r}, ${g}, ${b})`
}
function calcWaveformColors() {
    const waveColor = getThemeColor()
    const progressColor = darkenColor(waveColor)
    return { waveColor, progressColor }
}

const observer = new MutationObserver(() => {
    surfers.forEach(surfer => {
        surfer.setOptions(calcWaveformColors());
    })
});

observer.observe(document.querySelector('meta[name="theme-color"]'), {
  attributes: true,
  attributeFilter: ['content']
});
"""
            else:
                js += """
function calcWaveformColors() {
    return { }
}
"""
            # add wavesurfer instances for each audio element
            for container_id, audio_id, src_path in surfers_data:
                num = re.search(r'\d+', container_id).group(0)
                js += f"""
surfer{num} = WaveSurfer.create({{ ...options, ...calcWaveformColors(), ...{{
    container: document.querySelector('#{container_id}'),
    media: document.querySelector('#{audio_id}'),
    url: '{src_path}',
}} }})
surfer{num}.on('click', () => {{
    surfer{num}.play()
}})
surfers.push(surfer{num})
"""
            
            # inject the instantiation script at the end of the body element
            surfer_script = soup.new_tag('script')
            surfer_script.string = f"""
window.addEventListener('load', e => {{
{js}
}});
"""
            html = html.replace('</body>', str(surfer_script) + '\n</body>')
            # soup.body.append()

            # inject the wavesurfer library at the end of the head element
            lib_script = soup.new_tag('script')
            lib_script['src'] = "https://unpkg.com/wavesurfer.js@7"
            html = html.replace('</head>', str(lib_script) + '\n</head>')

        return html
