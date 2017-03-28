# encoding: utf-8
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging

try:
    from ckan.common import config # CKAN 2.7 and later
except ImportError:
    from pylons import config # CKAN 2.7 and later

log = logging.getLogger(__name__)

def get_hero_images():
    resources = []
    try:
        package_id = config.get('ckanext.heroslider.package_id', 'hero-slider-images')
        result = toolkit.get_action('package_show')({}, {'id': package_id})
        resource_list = result.get('resources')
        for item in resource_list:
            if item.get('format') in ['JPEG','PNG']:
                if item.get('url'):
                    resources.append(item.get('url'))
    except:
        log.debug('Getting Hero images failed')
    return resources

class HerosliderPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'heroslider')

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_hero_images': get_hero_images,
        }
