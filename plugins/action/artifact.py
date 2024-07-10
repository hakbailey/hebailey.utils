import json

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        self._supports_check_mode = False
        super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()
        module_return = self._execute_module(
            module_name="hebailey.utils.artifact",
            module_args=module_args,
            task_vars=task_vars,
            tmp=tmp,
        )

        artifact_data = module_return["artifact_data"]

        extra_vars = self._task._variable_manager.extra_vars
        artifact_data.update({"extra_vars": extra_vars})

        data_filepath = module_return.pop("datafile_path")
        with open(data_filepath, "w", encoding="utf-8") as data_out:
            data_out.write(json.dumps(artifact_data))

        return module_return
