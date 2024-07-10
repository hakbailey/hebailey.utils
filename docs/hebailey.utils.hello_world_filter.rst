.. _hebailey.utils.hello_world_filter:


**************************
hebailey.utils.hello_world
**************************

**Demo filter plugin that returns a Hello message.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This is a demo filter plugin designed to return Hello message.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Value specified here is appended to the Hello message.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    # hello_world filter example

    - name: Display a hello message
      ansible.builtin.debug:
        msg: "{{ 'ansible-creator' | hebailey.utils.hello_world }}"




Status
------


Authors
~~~~~~~

- Hebailey Utils


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
