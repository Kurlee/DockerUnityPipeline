import os

import yaml
from jinja2 import Template


class GitlabCiGenerator(object):
    default_dockerfile_name = 'unitysetup'

    def get_rendered_ci_template(self):
        context = {
            "versions": self.get_unity_versions() or {},
            "platforms": self.get_unity_platforms()
        }
        return self.render_template(self.get_ci_yaml_template(), context)

    @staticmethod
    def get_ci_yaml_template():
        base_dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
        return os.path.join(base_dirname, "gitlab-ci.jinja2")

    def get_unity_versions(self):
        unity_versions = self.get_unity_versions_path()
        with open(unity_versions, "r") as f:
            unity_versions = yaml.safe_load(f.read())
        unity_versions = self.get_versions_with_platforms(unity_versions)
        return self.set_dockerfile_to_unity_versions(unity_versions)

    @staticmethod
    def get_unity_versions_path():
        base_dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
        unity_versions = os.path.join(base_dirname, "unity_versions.yml")
        return unity_versions

    def get_versions_with_platforms(self, unity_versions):
        unity_versions_with_platforms = {}
        for version_key, version in unity_versions.items():
            if 'legacy' not in version or ('legacy' in version and not version.legacy):
                unity_versions_with_platforms[version_key] = {
                    "platforms": {**self.get_unity_platforms()},
                    "base_components": self.get_unity_base_components(),
                    **unity_versions[version_key],
                }
        return unity_versions_with_platforms

    def set_dockerfile_to_unity_versions(self, unity_versions):
        for version_key, version in unity_versions.items():
            for platform_key, _ in version.get('platforms', {}).items():
                unity_versions[version_key]['platforms'][platform_key]['dockerfile_name'] = \
                    self.get_dockerfile_name_to_use(platform_key, version)
        return unity_versions

    def get_dockerfile_name_to_use(self, platform, version):
        script_dirname = os.path.dirname(os.path.realpath(__file__))
        base_folder = os.path.join(script_dirname, '../../')
        dockerfile_name = version.get('dockerfile_name', self.default_dockerfile_name)
        base_dockerfile = f'{dockerfile_name}'

        platform_dockerfile_name = f'{dockerfile_name}-{platform}'
        platform_dockerfile = f'{platform_dockerfile_name}.Dockerfile'
        platform_dockerfile_path = os.path.join(base_folder, platform_dockerfile)

        if os.path.isfile(platform_dockerfile_path):
            return platform_dockerfile_name
        else:
            return base_dockerfile

    @staticmethod
    def get_unity_base_components():
        return "Unity,Windows,Windows-Mono,Mac,Mac-Mono,WebGL"

    @staticmethod
    def get_unity_platforms():
        return {
            "unity": {"components": "Unity"},
            "windows": {"components": "Unity,Windows,Windows-Mono"},
            "mac": {"components": "Unity,Mac,Mac-Mono"},
            "ios": {"components": "Unity,iOS"},
            "android": {"components": "Unity,Android"},
            "webgl": {"components": "Unity,WebGL"},
            "facebook": {"components": "Unity,Facebook-Games"},
        }

    @staticmethod
    def render_template(yaml_template, context):
        with open(yaml_template, "r") as f:
            template = Template(f.read())
        return template.render(context)

    def print(self):
        print("# !!! Do not edit this file manually, see ci-generator folder !!!")
        print(self.get_rendered_ci_template())
