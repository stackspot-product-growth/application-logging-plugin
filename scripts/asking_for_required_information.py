import yaml
import os
import re
from templateframework.metadata import Metadata
from questionary import questionary
from yaml.loader import SafeLoader


def run(metadata: Metadata = None):
    define_initial_configuration(metadata)

    request_inputs(metadata)

    setup_computed_inputs(metadata)


def request_inputs(metadata):
    request_project_name(metadata)
    request_spring_boot_version(metadata)
    request_java_version(metadata)
    request_project_artifact_id(metadata)
    request_project_group_id(metadata)
    request_build_tool(metadata)
    request_docker_compose_information_when_app_was_not_created_by_stackspot(metadata)


def define_initial_configuration(metadata):
    set_if_app_was_created_by_stackspot(metadata)
    set_if_docker_compose_exists(metadata)


def request_project_name(metadata):
    if "project_name" not in metadata.global_inputs:
        project_name = questionary.text(message="Inform the project name",
                                        validate=validate_project_name).unsafe_ask()
        metadata.global_inputs["project_name"] = project_name


def request_spring_boot_version(metadata):
    if "spring_boot_version" not in metadata.global_inputs:
        spring_boot_version = questionary.select("Select spring boot version", choices=["2.7.2", "3.0.1"]).unsafe_ask()
        metadata.global_inputs["spring_boot_version"] = spring_boot_version


def request_java_version(metadata):
    if "project_java_version" not in metadata.global_inputs:
        available_java_versions = ["17"]
        if metadata.global_inputs["spring_boot_version"] < '3':
            available_java_versions.append("11")
            available_java_versions.append("8")

        project_java_version = questionary.select("Select the Java version",
                                                  choices=available_java_versions).unsafe_ask()
        metadata.global_inputs["project_java_version"] = project_java_version


def request_project_artifact_id(metadata):
    if "project_artifact_id" not in metadata.global_inputs:
        project_artifact_id = questionary.text(message="Inform the project artifact ID",
                                               validate=validate_project_artifact_id,
                                               default=metadata.global_inputs["project_name"]).unsafe_ask()
        metadata.global_inputs["project_artifact_id"] = project_artifact_id


def request_project_group_id(metadata):
    if "project_group_id" not in metadata.global_inputs:
        project_group_id = questionary.text(message="Enter the base package for the project",
                                            instruction="(E.g: br.com.org)",
                                            validate=validate_java_package_name).unsafe_ask()
        metadata.global_inputs["project_group_id"] = project_group_id


def setup_computed_inputs(metadata):
    create_computed_inputs_for_project_configuration(metadata)
    define_package_dir(metadata)
    should_create_docker_compose(metadata)


def request_build_tool(metadata):
    if "build_tool" not in metadata.global_inputs:
        build_tool = questionary.select("Select the project build tool", choices=["Gradle", "Maven"]).unsafe_ask()
        metadata.global_inputs["build_tool"] = build_tool


def create_computed_inputs_for_project_configuration(metadata):
    build_tool = metadata.global_inputs["build_tool"]
    spring_boot_version = metadata.global_inputs["spring_boot_version"]
    project_java_version = metadata.global_inputs["project_java_version"]
    if int(project_java_version) == 8:
        metadata.computed_inputs["project_configuration"] \
            = f"{build_tool}:{spring_boot_version}:java{project_java_version}"
    else:
        metadata.computed_inputs["project_configuration"] \
            = f"{build_tool}:{spring_boot_version}"


def should_create_docker_compose(metadata):
    metadata.computed_inputs["is_application_created_by_stackspot_or_docker_compose_isnot_present"] = \
        is_application_created_by_stackspot(metadata) or not is_the_docker_compose_exists(metadata)


def define_package_dir(metadata):
    if "package_dir" not in metadata.global_computed_inputs:
        replaced_project_name = metadata.global_inputs["project_name"].replace('-', '')
        project_group_id = metadata.global_inputs["project_group_id"]
        metadata.global_computed_inputs["package_dir"] = f"{project_group_id}.{replaced_project_name}".replace('.', '/')
        metadata.global_computed_inputs["base_package"] = f"{project_group_id}.{replaced_project_name}"


def request_docker_compose_information_when_app_was_not_created_by_stackspot(metadata):
    if check_if_docker_compose_application_service_name_should_be_requested(metadata):
        docker_compose = load_yaml(f"{metadata.target_path}/docker-compose.yaml")
        if docker_compose['services'].keys():
            docker_compose_application_service_name = select_docker_compose_application_service_name(docker_compose)

            metadata.global_inputs["docker_compose_application_service_name"] = \
                docker_compose_application_service_name
    else:
        if not is_docker_compose_service_name_already_requested(metadata):
            metadata.global_inputs["docker_compose_application_service_name"] \
                = metadata.global_inputs["project_artifact_id"]


def check_if_docker_compose_application_service_name_should_be_requested(metadata):
    return is_the_docker_compose_exists(metadata) and not is_application_created_by_stackspot(metadata) \
        and not is_docker_compose_service_name_already_requested(metadata)


def is_docker_compose_service_name_already_requested(metadata):
    return "docker_compose_application_service_name" in metadata.global_inputs


def is_the_docker_compose_exists(metadata):
    return metadata.inputs["is_the_docker_compose_exists"]


def set_if_docker_compose_exists(metadata):
    metadata.inputs["is_the_docker_compose_exists"] = os.path.exists(f"{metadata.target_path}/docker-compose.yaml")


def is_application_created_by_stackspot(metadata):
    return metadata.global_inputs["is_application_created_by_stackspot"]


def select_docker_compose_application_service_name(docker_compose):
    return questionary.select("Select the application service name in your docker-compose.yaml ",
                              choices=docker_compose[
                                  'services'].keys()).unsafe_ask()


def set_if_app_was_created_by_stackspot(metadata):
    if "is_application_created_by_stackspot" not in metadata.global_inputs:
        if os.path.exists(f"{metadata.target_path}/.stk/stk.yaml"):
            metadata.global_inputs["is_application_created_by_stackspot"] = True
        else:
            metadata.global_inputs["is_application_created_by_stackspot"] = False


# def create_default_inputs_docker_controller(metadata):
#     if "docker_compose_application_service_name" not in metadata.global_inputs or \
#             not is_docker_compose_exists(metadata):
#         metadata.global_inputs["docker_compose_application_service_name"] = None


def validate_java_package_name(value):
    if re.search("(^[a-zA-Z_\d.]*[a-zA-Z_\d]$)", value) is None:
        return "Invalid package name." \
               " Check the standardized java convention" \
               " https://docs.oracle.com/javase/tutorial/java/package/namingpkgs.html"
    else:
        return True


def validate_project_name(value):
    if re.search("(^[\w\d-]+$)", value) is None:
        return "Invalid project name."
    return True


def validate_project_artifact_id(value):
    if re.search("(^[a-zA-Z-_\d]*$)", value) is None:
        return "Invalid artifact id."
    return True


def load_yaml(file_path):
    with open(file_path) as yaml_file:
        return yaml.load(yaml_file, Loader=SafeLoader)


def write_yaml(file_path, yaml_data):
    with open(file_path, "w") as yaml_file:
        yaml.dump(yaml_data, yaml_file, sort_keys=False, default_flow_style=False)
