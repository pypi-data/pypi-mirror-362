#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (c) 2024 PAL Robotics S.L. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import datetime
from importlib.metadata import version
from jinja2 import Environment, select_autoescape, FileSystemLoader
import random
import re
import string
import sys
from pathlib import Path
import shutil

import rpk

SELF_NAME = "rpk"

# not using ament, so that is also work outside of a ROS environment
PKG_PATH = (
    Path(rpk.__file__).parent.parent.parent.parent.parent / "share" /
    "rpk"
)

SKILL_TEMPLATES = {
    "skill_definition": {
        "tpl_paths": ["skills/skill_definition/{{id}}_skill_msgs"],
        "prog_lang": "manifest",
        "short_desc": "template for a skill manifest and API",
        "post_install_help": "Check README.md in {path}/{id}_skill_msgs/ "
                             "edit {id}_skill_msgs/package.xml to edit your skill manifest.",
    },
    "base_cpp": {
        "tpl_paths": ["skills/base_cpp/{{id}}"],
        "prog_lang": "c++",
        "short_desc": "base skill template [c++]",
        "post_install_help": "Check README.md in {path}/{id}/ and "
                             "edit src/{id}/node_{id}.cpp and include/{id}/node_{id}.hpp "
                             "to implement your skill logic.",
        "skill_templates": [
            {"skill_definition": {"id": "{{id}}", "name": "{{id}} skill definition"}}
        ],
    },
    "base_python": {
        "tpl_paths": ["skills/base_python/{{id}}"],
        "prog_lang": "python",
        "short_desc": "base skill template [python]",
        "post_install_help": "Check README.md in {path}/{id}/ and "
                             "edit src/{id}/skill_impl.py to implement your skill logic.",
        "skill_templates": [
            {"skill_definition": {"id": "{{id}}", "name": "{{id}} skill definition"}}
        ],
    },
    "say_python": {
        "tpl_paths": ["skills/say_python/{{id}}"],
        "prog_lang": "python",
        "short_desc": "creates a custom implementation of the standard 'say' skill [python]",
        "post_install_help": "Check README.md in {path}/{id}/ and "
                             "edit src/{id}/skill_impl.py to implement your skill logic.",
    },
    "db_connector_python": {
        "tpl_paths": ["skills/db_connector_python/{{id}}"],
        "prog_lang": "python",
        "short_desc": "database connector mock-up [python]",
        "post_install_help": "Check README.md in {path}/{id}/ and "
                             "edit src/{id}/skill_impl.py to implement your skill logic.",
        "skill_templates": [{"skill_definition": {
            "id": "db",
            "name": "Skill definition for a custom database connector"
        }}],
    },
    "locate_cpp": {
        "tpl_paths": ["skills/locate_cpp/{{id}}"],
        "prog_lang": "c++",
        "short_desc": "example implementation of 'locate' skill [c++]",
        "post_install_help": "Check README.md in {path}/{id}/ and "
                             "edit src/{id}/node_{id}.cpp and include/{id}/node_{id}.hpp "
                             "to implement your skill logic.",
        "skill_templates": [{"skill_definition": {
            "id": "locate", "name": "Manifest of the 'locate' skill"
        }}],
    },
}

INTENT_EXTRACTOR_TEMPLATES = {
    "basic_chatbot": {
        "tpl_paths": ["intents/basic_chatbot/{{id}}"],
        "prog_lang": "python",
        "short_desc": "basic chatbot template [python]",
        "post_install_help": "Check README.md in {path}/{id}/ and "
                             "edit src/{id}/node_impl.py to implement your node logic.",
    },
    "llm_bridge_python": {
        "tpl_paths": ["intents/llm_connector_python/{{id}}"],
        "prog_lang": "python",
        "short_desc": "complete intent extraction example: LLM bridge using the OpenAI "
                      "API (ollama, chatgpt) [python]",
        "post_install_help": "Check README.md in {path}/{id}/ and "
                             "edit src/{id}/node_impl.py to implement your node logic.",
    },
}

TASK_TEMPLATES = {
    "base_python": {
        "tpl_paths": ["tasks/base_python/{{id}}", "tasks/task_msgs"],
        "prog_lang": "python",
        "short_desc": "base task template [python]",
        "post_install_help": "Check README.md in {path}/{id}/ and "
                             "edit src/{id}/task_impl.py to implement your task logic.",
    },
    "simple_ui": {
        "tpl_paths": ["tasks/simple_ui/{{id}}", "tasks/task_msgs"],
        "prog_lang": "python",
        "short_desc": "simple task template with a graphical user interface [python]",
        "post_install_help": "Check README.md in {path}/{id}/ and "
                             "edit src/{id}/task_impl.py to implement your task logic.",
    },
    "greet_task_python": {
        "tpl_paths": ["tasks/greet_task_python/{{id}}", "tasks/greet_task_msgs"],
        "prog_lang": "python",
        "short_desc": "'greet' task mock-up [python]",
        "post_install_help": "Check README.md in {path}/{id}/ and "
                             "edit src/{id}/task_impl.py to implement your task logic.",
        "skill_templates": [{"say_python": {"id": "say_skill", "name": "basic 'say' skill"}}],
    }
}

MISSION_CTRL_TEMPLATES = {
    "base_python": {
        "tpl_paths": ["mission_ctrls/base_python/{{id}}"],
        "prog_lang": "python",
        "short_desc": "base robot supervisor [python]",
        "post_install_help": "Check README.md in {path}/{id}/ and edit src/{id}/"
                             "mission_controller.py to customize your application logic.",
        "skill_templates": [{"say_python": {"id": "basic_say", "name": "basic 'say' skill"}}],
    },
    "base_intents_python": {
        "tpl_paths": ["mission_ctrls/base_intents_python/{{id}}"],
        "prog_lang": "python",
        "short_desc": "robot supervisor with pre-filled intent handlers [python]",
        "post_install_help": "Check README.md in {path}/{id}/ and edit src/{id}/"
                             "mission_controller.py to implement your application logic.",
    },
    "base_intents_ui_python": {
        "tpl_paths": ["mission_ctrls/base_intents_ui_python/{{id}}"],
        "prog_lang": "python",
        "short_desc": "robot supervisor with a GUI and pre-filled intent handlers [python]",
        "post_install_help": "Check README.md in {path}/{id}/ and edit src/{id}/"
                             "mission_controller.py to implement your application logic.",
        "task_templates": [{"simple_ui": {"id": "sample_gui_task", "name": "Sample GUI task"}}],
    },
    "chatbot_supervisor_python": {
        "tpl_paths": ["mission_ctrls/llm_supervisor_python/{{id}}"],
        "prog_lang": "python",
        "short_desc": "complete supervisor example, using a basic chatbot to manage interactions "
                      "with users [python]",
        "post_install_help": "Check README.md in ./{path}/ and edit src/{id}/"
                             "mission_controller.py to customize your application logic.",
        "task_templates": [{"greet_task_python": {"id": "greet_task", "name": "'greet' task"}}],
        "intent_extractor_templates": [{"basic_chatbot": {
            "id": "basic_chatbot",
            "name": "Basic Python chatbot"}}],
    },
    "llm_supervisor_python": {
        "tpl_paths": ["mission_ctrls/llm_supervisor_python/{{id}}"],
        "prog_lang": "python",
        "short_desc": "complete supervisor example, using LLMs to manage interactions with "
                      "users [python]",
        "post_install_help": "Check README.md in ./{path}/ and edit src/{id}/"
                             "mission_controller.py to customize your application logic.",
        "task_templates": [{"greet_task_python": {"id": "greet_task", "name": "'greet' task"}}],
        "intent_extractor_templates": [{"llm_bridge_python": {
            "id": "llm_bridge",
            "name": "LLM bridge"}}],
    }
}


APPLICATION_TEMPLATES = {
    "basic_chatbot_python": {
        "tpl_paths": ["apps/python/{{id}}"],
        "prog_lang": "python",
        "short_desc": "complete sample app, using a basic chatbot to interact with users. "
                      "It includes a supervisor and sample tasks and skills [python]",
        "post_install_help": "Check README.md in ./{path}/ to learn how to configure "
                             "and start your application.",
        "mission_ctrl_templates": [{"chatbot_supervisor_python": {
            "id": "chatbot_supervisor",
            "name": "Mission controller"}}],
    },
    "llm_chatbot_python": {
        "tpl_paths": ["apps/python/{{id}}"],
        "prog_lang": "python",
        "short_desc": "complete sample app, using LLM to interact with users. "
                      "It includes a supervisor and sample tasks and skills [python]",
        "post_install_help": "Check README.md in ./{path}/ to learn how to configure "
                             "and start your application.",
        "mission_ctrl_templates": [{"llm_supervisor_python": {
            "id": "llm_supervisor",
            "name": "LLM-based mission controller"}}],
    }
}

TEMPLATES_FAMILIES = {
    "intent": {"src": INTENT_EXTRACTOR_TEMPLATES,
               "name": "intent extractor",
               "cmd": "intent",
               "help": "perception module that extracts intents from user input. "
               "Example: a chatbot"},
    "skill": {"src": SKILL_TEMPLATES,
              "name": "skill",
              "cmd": "skill",
              "help": "short-term 'atomic' robot action, to be re-used by tasks and mission "
                      "controllers. Examples: 'go to', 'say', 'perform pre-recorded motion'"},
    "task": {"src": TASK_TEMPLATES,
             "name": "task",
             "cmd": "task",
             "help": "time-limited robot activity, started by the mission controller. "
                     "Might use skills. Examples: 'greet person', 'fetch object'"},
    "mission": {"src": MISSION_CTRL_TEMPLATES,
                "name": "mission controller",
                "cmd": "mission",
                "help": "manages the whole behaviour of the robot. Examples: 'receptionist', "
                        "'waiter'"},
    "app": {"src": APPLICATION_TEMPLATES,
            "name": "application",
            "cmd": "app",
            "help": "complete application including a mission controller, a sample "
                    "task and skill, and sample resources"}
}

ROBOTS_NAMES = {"generic": "Generic robot",
                "generic-pal": "Generic PAL robot/simulator",
                "ari": "PAL ARI",
                "tiago": "PAL TIAGo",
                "tiago-pro": "PAL TIAGo Pro",
                "tiago-head": "PAL TIAGo Head"}
AVAILABLE_ROBOTS = list(ROBOTS_NAMES.keys())

FEAT_NAV = "navigation"
FEAT_VISION = "vision"
FEAT_SOCIAL = "social"
FEAT_COMMUNICATION = "communication"
FEAT_MANIPULATION = "manipulation"
FEAT_GESTURES = "gestures"
FEAT_EXPRESSIONS = "expressions"
FEAT_PAL_ARCH = "pal_arch"

ROBOTS_FEATURES = {
    "generic": [],
    "generic-pal": [FEAT_PAL_ARCH],
    "ari":         [FEAT_PAL_ARCH,
                    FEAT_NAV,
                    FEAT_VISION,
                    FEAT_SOCIAL,
                    FEAT_COMMUNICATION,
                    FEAT_GESTURES,
                    FEAT_EXPRESSIONS,
                    ],
    "tiago":       [FEAT_PAL_ARCH,
                    FEAT_NAV,
                    FEAT_VISION,
                    FEAT_SOCIAL,
                    FEAT_COMMUNICATION,
                    FEAT_MANIPULATION,
                    FEAT_GESTURES,
                    ],
    "tiago-pro":   [FEAT_PAL_ARCH,
                    FEAT_NAV,
                    FEAT_VISION,
                    FEAT_SOCIAL,
                    FEAT_COMMUNICATION,
                    FEAT_MANIPULATION,
                    FEAT_GESTURES,
                    FEAT_EXPRESSIONS],
    "tiago-head":  [FEAT_PAL_ARCH,
                    FEAT_VISION,
                    FEAT_SOCIAL,
                    FEAT_COMMUNICATION,
                    FEAT_EXPRESSIONS,
                    ],
}


TPL_EXT = "j2"


def random_id():
    rand_id = ''.join(random.choices(string.ascii_lowercase, k=5))
    print(f"Using random ID {rand_id}")
    return rand_id


def get_intents():

    intents = []

    try:
        from rosidl_runtime_py import get_interface_path
        from rosidl_adapter.parser import parse_message_file
    except ImportError:
        print(
            "rosidl_runtime_py or rosidl_adapter are not installed -- we "
            "cannot automatically generate the list of available intents"
        )
        return intents

    try:
        msg_def = parse_message_file(
            'hri_actions_msgs',
            get_interface_path('hri_actions_msgs/msg/Intent'))
    except LookupError:
        # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        # message = template.format(type(ex).__name__, ex.args)
        # print(message)
        print(
            "Intent.msg not found. You can install it with 'apt install "
            "pal-alum-hri-actions-msgs'.\nFor now, not generating the list "
            "of available intents."
        )
        return intents

    # We will only extract the available intents for now, not the additional
    # fields (description and thematic roles) since rosidl parser ignores
    # comments below the message fields. To solve this, we should place the
    # long description of the intents before describing the msg fields.
    for c in msg_def.constants:
        if "__intent_" in c.value:
            intents.append({'intent': c.name,
                            'description': '',
                            'required_thematic_roles': [],
                            'optional_thematic_roles': []})
    if not intents:
        print(
            "Intent.msg empty :-( Not generating the intents handling code")
        return intents

    return intents


def interactive_create(id=None,
                       name=None,
                       family=None,
                       template=None,
                       robot=None,
                       yes=False):

    # apply subset of topic name rules to the ID, since it may be used in pkg topics names
    valid_id = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")

    if not id and yes:
        id = random_id()

    try:
        while not id:
            id = input(
                "ID of your application? (must be a valid ROS identifier without "
                "spaces or hyphens. eg 'robot_receptionist')\n"
            )

            if not valid_id.fullmatch(id):
                print("The chosen ID can only contain alphanumeric or '_' characters,"
                      " and cannot start with a number.")
                id = None

        if not name and not yes:
            name = input(
                "Full name of your skill/application? (eg 'The Receptionist Robot' or "
                "'Database connector', press Return to use the ID. You can change it later)\n"
            )

        if not name:
            name = id

        # get the user to choose between mission controller, skill or full
        # application
        while not family:
            print("\nWhat content do you want to create?")
            for idx, family in enumerate(TEMPLATES_FAMILIES.keys()):
                print("%s: %s" % (idx + 1, TEMPLATES_FAMILIES[family]["name"]))

            try:
                choice = int(input("\nYour choice? "))
                family = list(TEMPLATES_FAMILIES.keys())[choice - 1]
            except (ValueError, IndexError):
                family = ""

        tpls = TEMPLATES_FAMILIES[family]["src"]

        if not tpls:
            print("No templates available for %s. Exiting." % family)
            sys.exit(1)

        while not template:
            print("\nChoose a template:")
            for idx, tpl in enumerate(tpls.keys()):
                print("%s: %s" %
                      (idx + 1, tpls[tpl]["short_desc"]))

            try:
                if len(tpls) == 1:
                    # if only one template available, make it the default choice
                    choice = int(input(
                        "\nYour choice? (default: 1: "
                        f"{tpls[list(tpls.keys())[0]]['short_desc']}) ").strip() or 1)
                else:
                    choice = int(input("\nYour choice? ").strip())

                template = list(tpls.keys())[choice - 1]
            except (ValueError, IndexError):
                template = ""

        if not robot and yes:
            robot = AVAILABLE_ROBOTS[0]

        while not robot:
            print("\nWhat robot are you targeting?")
            for idx, r in enumerate(AVAILABLE_ROBOTS):
                print(f"{idx + 1}: {ROBOTS_NAMES[r]} ({r})")

            try:
                choice = int(
                    input(f"\nYour choice? (default: 1: {AVAILABLE_ROBOTS[0]}) ").strip() or 1)

                robot = AVAILABLE_ROBOTS[choice - 1]
            except (ValueError, IndexError):
                robot = ""
    except KeyboardInterrupt:
        sys.exit(1)

    return id, name, family, template, robot


def generate_skeleton(data, family, tpl_name, robot, root):
    print(f"Generating {family} skeleton in {root.resolve()}...")
    tpl = TEMPLATES_FAMILIES[family]["src"][tpl_name]

    data["dependencies"] = []

    # if needed, first generate the skeletons for the missions, skills and tasks
    # referenced in the template
    for additional_tpl in ["intent_extractor_templates",
                           "skill_templates",
                           "task_templates",
                           "mission_ctrl_templates"]:
        if additional_tpl in tpl:
            type = additional_tpl.split("_")[0]
            for a_tpl in tpl[additional_tpl]:
                tpl_name = list(a_tpl.keys())[0]
                a_data = dict(data)
                a_data["id"] = a_tpl[tpl_name]["id"].replace(
                    "{{id}}", data["id"]).replace("{{Id}}", data["Id"])
                a_data["Id"] = string.capwords(
                    a_data["id"], '_').replace("_", "")
                data["dependencies"].append(a_data["id"])
                a_data["name"] = a_tpl[tpl_name]["name"]
                generate_skeleton(a_data, type, tpl_name, robot, root)

    # then generate the skeleton for the current template
    tpl_paths = [PKG_PATH / "tpl" / p for p in tpl["tpl_paths"]]

    for tpl_path in tpl_paths:
        env = Environment(
            loader=FileSystemLoader(str(tpl_path)),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        j2_tpls = env.list_templates()

        if not j2_tpls:
            print(
                "Error! no app template found for %s. I was looking for "
                f"template files under <%s>. It seems {SELF_NAME} is not correctly "
                "installed."
                % (tpl, tpl_path)
            )
            sys.exit(1)

        for j2_tpl_name in j2_tpls:
            if (("pages_only_ari" in j2_tpl_name) and (robot not in j2_tpl_name)):
                continue

            # 'base' is the name of the package directory
            base = root / \
                tpl_path.name.replace("{{id}}", data["id"]).replace(
                    "{{Id}}", data["Id"])
            base.mkdir(parents=True, exist_ok=True)

            # Non-template file, copy file as is
            if j2_tpl_name.split('.')[-1] != TPL_EXT:
                source_filename = tpl_path / j2_tpl_name
                filename = base / j2_tpl_name
                filename.parent.mkdir(parents=True, exist_ok=True)
                print(f"Creating {filename}...")
                shutil.copy(source_filename, filename)
            else:
                j2_tpl = env.get_template(j2_tpl_name)
                j2_tpl_name = j2_tpl_name.replace(
                    "{{id}}", data["id"]).replace("{{Id}}", data["Id"])

                filename = base / j2_tpl_name[: -(1 + len(TPL_EXT))]
                filename.parent.mkdir(parents=True, exist_ok=True)
                print(f"Creating {filename}...")
                with open(filename, "w") as fh:
                    fh.write(j2_tpl.render(data))

    print("\n\033[32;1mDone!")
    print("\033[33;1m")
    print(tpl["post_install_help"].format(
        path=root.resolve(), id=data["id"]))
    print("\033[0m")


def main(args=sys.argv[1:]):

    parser = argparse.ArgumentParser(
        description="Generate and manage application skeletons for ROS 2-based "
                    "robots"
    )

    parser.add_argument('--version', action='version',
                        version=f'{SELF_NAME} {version(SELF_NAME)}')

    subparsers = parser.add_subparsers(dest="command")

    #######################################################################################
    # create command

    create_parser = subparsers.add_parser(
        "create", help="Create new application/task/skill skeletons"
    )

    create_parser.add_argument(
        "-r",
        "--robot",
        choices=AVAILABLE_ROBOTS,
        type=str,
        nargs="?",
        help="target robot",
    )

    family_subparsers = create_parser.add_subparsers(dest="family")
    for family in TEMPLATES_FAMILIES.keys():
        f_parser = family_subparsers.add_parser(
            family, help=TEMPLATES_FAMILIES[family]["help"]
        )

        f_parser.add_argument(
            "-y",
            "--yes",
            action="store_true",
            help="do not ask questions, automatically accept defaults",
        )

        f_parser.add_argument(
            "-t",
            "--template",
            choices=TEMPLATES_FAMILIES[family]["src"].keys(),
            type=str,
            nargs="?",
            help="Template to use.",
        )

        f_parser.add_argument(
            "-i",
            "--id",
            type=str,
            nargs="?",
            help="ID of your application. Must be a valid ROS2 identifier, without "
            "spaces or hyphens.",
        )

    create_parser.add_argument(
        "-p",
        "--path",
        type=str,
        nargs="?",
        const=".",
        default=".",
        help="path of the directory where the skeleton will be generated "
             "(default: .)",
    )

    #######################################################################################
    # list command

    list_tpl_parser = subparsers.add_parser(
        "list", help="List all available templates"
    )

    list_tpl_parser.add_argument(
        "-s",
        "--short",
        action="store_true",
        help="only display the template' names",
    )

    #######################################################################################
    #######################################################################################

    args = parser.parse_args(args)

    if not args.command:
        print(
            f"You must select a command.\nType '{SELF_NAME} --help' for details.")
        sys.exit(1)

    if args.command == "create":

        if not hasattr(args, "template"):
            print("You must select a type of content.\n"
                  f"Type '{SELF_NAME} create --help' for details.")
            sys.exit(1)

        intents = get_intents()

        id, name, family, tpl_name, robot = interactive_create(
            args.id,
            name=None,
            family=args.family,
            template=args.template,
            robot=args.robot,
            yes=args.yes)

        data = {"id": id,
                "Id": string.capwords(id, '_').replace("_", ""),
                "name": name,
                "intents": intents,
                "robot": robot,
                "robot_name": ROBOTS_NAMES[robot],
                "features": ROBOTS_FEATURES[robot],
                "author": "TODO",
                "year": datetime.datetime.now().year}

        root = Path(args.path)
        root.mkdir(parents=True, exist_ok=True)

        generate_skeleton(data, family, tpl_name, robot, root)

    elif args.command == "list":

        for family in TEMPLATES_FAMILIES.keys():
            tpls = TEMPLATES_FAMILIES[family]
            if not args.short:
                print(
                    f"\n# {tpls['name']} templates (rpk create {tpls['cmd']} ...):")
            for tpl in tpls["src"].keys():
                if args.short:
                    print(f"{family}/{tpl}")
                else:
                    print(
                        f" - {tpl}: {tpls['src'][tpl]['short_desc']}")


if __name__ == "__main__":
    main()
