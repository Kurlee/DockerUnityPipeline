# Unity3d docker image

[![pipeline status](https://gitlab.com/gableroux/unity3d/badges/master/pipeline.svg)](https://gitlab.com/gableroux/unity3d/commits/master) [![Docker Stars](https://img.shields.io/docker/stars/gableroux/unity3d.svg)](https://hub.docker.com/r/gableroux/unity3d/) [![Docker Pulls](https://img.shields.io/docker/pulls/gableroux/unity3d.svg)](https://hub.docker.com/r/gableroux/unity3d/) [![Docker Automated build](https://img.shields.io/docker/automated/gableroux/unity3d.svg)](https://hub.docker.com/r/gableroux/unity3d/) [![Image](https://images.microbadger.com/badges/image/gableroux/unity3d.svg)](https://microbadger.com/images/gableroux/unity3d) [![Version](https://images.microbadger.com/badges/version/gableroux/unity3d.svg)](https://microbadger.com/images/gableroux/unity3d)

This project builds docker images for all unity versions and their components. It contains a script that generates a `.gitlab-ci.yml` that is used to build and publish all of the images. All supported versions can be found in [`ci-generator/unity_versions.yml`](ci-generator/unity_versions.yml) (latest built images) and [`ci-generator/unity_versions.old.yml`](ci-generator/unity_versions.old.yml) (already built images).

## Things to consider

These docker images run in a shell so you don't have access to Unity's UI. This docker image is intended to run unity commands with the **command line**. You can use it for running **tests** and **creating builds**.

## Usage

This docker image is intended to be used with a CI. An example project using unity3d in a docker image can be found at **[gableroux/unity3d-gitlab-ci-example](https://gitlab.com/gableroux/unity3d-gitlab-ci-example)**. Go there and follow its instructions if you'd like to use this image in your project.

### Build the image

Images are built automatically by the CI based on `.gitlab-ci.yml` content that is generated by **[./ci-generator](./ci-generator)**. If you'd like to build the images by yourself, you can do something like this:

```bash
docker build -t gableroux/unity3d:latest ./docker/ -f ./docker/unitysetup.Dockerfile
```

But at this point, you should fork the project, generate the the `.gitlab-ci.yml` and let gitlab build the images for you. By default, the images will be published to your fork's registry.

### Run the image

```bash
docker run -it --rm \
  -v "$(pwd):/root/project" \
  gableroux/unity3d:latest \
  xvfb-run --auto-servernum --server-args='-screen 0 640x480x24' \
  /opt/Unity/Editor/Unity -projectPath /root/project
```

## How it all started

This initial docker image was first based on [GitLab CI with Unity3D in Docker](https://www.projects.science.uu.nl/DGKVj16/blog/gitlab-ci-with-unity3d-in-docker/) but changed a lot since then, thanks to contributors!

## My version is missing, what can I do?

Have a look at the issues or merge requests first, then follow instructions in [ci-generator](./ci-generator).

## How are these images published to docker hub?

Refer to this [QA](https://stackoverflow.com/questions/45517733/how-to-publish-docker-images-to-docker-hub-from-gitlab-ci). tldr; I only updated a few environment variables in gitlab-ci settings, this is optional.

## License

[MIT](LICENSE.md) © [Gabriel Le Breton](https://gableroux.com)

