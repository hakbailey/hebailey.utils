import json
import os
import random
import shutil
import string

from pathlib import Path

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.parameters import env_fallback


DOCUMENTATION = """
    name: artifact
    description:
        - Saves artifacts
    short_description: Saves artifacts
    author: Helen Bailey (@hakbailey)
    options:
      artifacts_dir:
        type: path
        required: True
        env:
          - name: ANSIBLE_ARTIFACT_STORAGE_PATH
        description:
          - Artifact storage path where the module will temporarily
            save the artifact.
      name:
        type: string
        description:
            - Name for the artifact.
      path:
        type: path
        description:
          - Path to file to store as artifact.
"""


def main():
    module = AnsibleModule(
        argument_spec=dict(
            artifacts_dir=dict(
                type="path",
                fallback=(
                    env_fallback,
                    ["ANSIBLE_ARTIFACT_STORAGE_PATH", "AWX_ISOLATED_DATA_DIR"],
                ),
                required=True,
            ),
            name=dict(type="str"),
            path=dict(type="path", required=True),
        ),
        supports_check_mode=False,
    )
    result = dict()

    artifacts_dir = module.params["artifacts_dir"] or os.getcwd()
    if not artifacts_dir.endswith("job_artifacts"):
        artifacts_dir = os.path.join(artifacts_dir, "job_artifacts")
    files_dir = os.path.join(artifacts_dir, "files")
    data_dir = os.path.join(artifacts_dir, "data")
    for path in (artifacts_dir, files_dir, data_dir):
        if not os.path.exists(path):
            os.mkdir(path, 0o700)

    random_id = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=10),
    )

    filepath = module.params["path"]
    filename = os.path.basename(filepath)
    new_filename = f"{random_id}_{filename}"
    new_filepath = os.path.join(
        files_dir,
        new_filename,
    )
    shutil.copy(filepath, new_filepath)
    result.update({"artifact_path": new_filepath})

    artifact_name = module.params["name"] or Path(filename).stem
    artifact_data = dict(artifact_name=artifact_name)
    artifact_data.update(
        {
            "artifact_path": os.path.join(
                "job_artifacts",
                "files",
                new_filename,
            ),
        },
    )

    artifact_data.update({"env": dict(os.environ.items())})

    data_filename = f"{random_id}_{artifact_name}_data.json"
    data_filepath = os.path.join(data_dir, data_filename)
    with open(data_filepath, "w", encoding="utf-8") as data_out:
        data_out.write(json.dumps(artifact_data))
    result.update(
        {
            "data_path": os.path.join(
                "job_artifacts",
                "data",
                data_filename,
            ),
        },
    )

    result.update(artifact_data)
    result.update({"changed": True})

    module.exit_json(**result)


if __name__ == "__main__":
    main()
