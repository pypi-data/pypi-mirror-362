import mkdocs
import re
import xml.etree.ElementTree as ET

class AudioTag(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ('autoplay', mkdocs.config.config_options.Type(bool, default=False)),
        ('controls', mkdocs.config.config_options.Type(bool, default=True)),
        ('loop', mkdocs.config.config_options.Type(bool, default=False)),
        ('muted', mkdocs.config.config_options.Type(bool, default=False)),
        ('preload', mkdocs.config.config_options.Type(str, default='metadata')),
        ('width', mkdocs.config.config_options.Type(str, default='100%'))
    )

    def on_page_markdown(self, markdown, page, config, files):
        # this finds all audio files noted like this: ![audio/mp3](path/to/my/file.mp3)
        # capturing the ones that are written on consecutive lines together
        # (i.e. with no spaces between lines)
        audio_elements = re.finditer(r'^(?:!\[audio/.+?]\(.+?\)\n)+', markdown, re.M)
        
        num = 0
        for match in audio_elements:
            old_tag = match.group(0)
            sources = re.findall(r'!\[(.+)\]\((.+)\)', old_tag)

            container = ET.Element('div', attrib={'class': 'audio-container', 'id': f'audio-container-{num}'})

            tag = ET.Element('audio', attrib={
                    'preload': self.config['preload'],
                    'id': 'audio-tag' + str(num),
                 })

            tag.set('style',f'width:{self.config['width']}')

            # Boolean attributes
            for attribute in ['autoplay', 'controls', 'loop', 'muted']:
                if self.config[attribute]:
                    tag.set(attribute, '')

            for mimetype, file in sources:
                element_class = mimetype.replace('audio/', '')
                ET.SubElement(tag, 'source', attrib={
                    'src': '../' + file,
                    'type': mimetype,
                    'class': element_class
                    })
            
            container.append(tag)

            new_tag = ET.tostring(container, encoding='unicode', method='html') + '\n'
            
            markdown = markdown.replace(old_tag, new_tag, 1)
            num += 1        
        return markdown
