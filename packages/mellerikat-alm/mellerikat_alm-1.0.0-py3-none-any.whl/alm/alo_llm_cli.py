import os
import json
import getpass
import requests
from dotenv import dotenv_values
from alm.utils import print_job_info, update_file_keys_in_json, zip_current_directory

# read_token_from_file 삭제

def handle_response(response, success_message, keys=None):
    def get_value_from_path(data, path):
        """Helper function to retrieve value from nested JSON using path as a list of keys."""
        for key in path:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data

    if response.status_code == 200:
        print(success_message)
        data = response.json()
        if keys:
            for key_path in keys:
                if isinstance(key_path, (list, tuple)):
                    value = get_value_from_path(data, key_path)
                    if value is not None:
                        print(f"{(key_path[1])}: {value}")
                    else:
                        print(f"Path {' -> '.join(key_path)} not found in response.")
                else:
                    if key_path in data:
                        print(f"{key_path}: {data[key_path]}")
                    else:
                        print(f"Key '{key_path}' not found in response.")
        else:
            # If no keys provided, print the whole JSON response
            print(data)
    else:
        print(f"Error {response.status_code}: ", response.text)

# Usage example:
# Assuming 'response' is an object with the response data
# handle_response(response, "Success: ", keys=["aipack_activate_url", ["stream_history_info", "name"], ["stream_history_info", "creator"]])

class ALC():
    def __init__(self, url, settings):
        self.url = url
        self.settings = settings

    def api(self, args):
        from alm.alo_llm import Alo
        from alm.model import settings
        settings.computing = 'api'
        alo = Alo()
        alo.run()

    def login(self, args):
        args.id = input("Please enter your AI Conductor ID: ")
        args.password = getpass.getpass("Please enter your AI Conductor password: ")

        login_url = f"{self.url}/api/v1/auth/login"
        login_data = {"username": args.id, "password": args.password}
        response = requests.post(login_url, data=login_data)

        if response.status_code != 200:
            print("Failed to obtain access token:", response.status_code, response.text)
            return

        tokens = response.json()
        access_token = tokens['access_token']
        workspace_return = tokens['user']['workspace']

        update_file_keys_in_json('access_token', access_token, initialize=True)
        print("Login success")

        workspace_list = [workspace['name'] for workspace in workspace_return]
        for workspace in workspace_return:
            update_file_keys_in_json(workspace['name'], workspace['id'])

        print(f'You can access these workspaces: {workspace_list}')

        if len(workspace_list) == 1:
            default_workspace = workspace_list[0]
            print(f"Default workspace: {default_workspace}")
        else:
            default_workspace = input("Please input default workspace: ")

            if default_workspace not in workspace_list:
                raise ValueError("Please check default workspace name !!")

        update_file_keys_in_json('default_ws', default_workspace)
        print(f"Default workspace: {default_workspace}")

    def register(self, args):
        workspace_id = self._check_ws(args.workspace)
        token = self._read_token_from_file('access_token')
        headers = {"Authorization": f'Bearer {token}'}

        if args.update:

            ai_pack_name = args.update

            register_list_url = f"{self.url}/api/v1/workspaces/{workspace_id}/aipacks"
            response = requests.get(register_list_url, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                api_names = {solution['name']: solution['id'] for solution in response_data['solutions']}
                solution_id = api_names.get(ai_pack_name, None)

                apilist_url = f"{self.url}/api/v1/workspaces/{workspace_id}/aipacks/{solution_id}/versions"

                api_name = ai_pack_name if ai_pack_name else input("Service API name: ")
                api_overview = input("Service API description overview: ")
                zip_current_directory(f'{api_name}.zip', exclude_files=['.env', '.token', '.venv', '.workspace', '__pycache__'])

                from alm.__version__ import __version__
                metadata = {
                    "metadata_version": "1.2",
                    "name": api_name,
                    "description": {
                        "title": api_name,
                        "alo_version": str(__version__),
                        "contents_name": api_name,
                        "contents_version": "1.0.0",
                        "inference_build_type": "amd64",
                        "overview": api_overview,
                        "detail": [
                            {
                                "title": "title001",
                                "content": "content001"
                            },
                            {
                                "title": "title002",
                                "content": "content002"
                            }
                        ]
                    },
                    "ai_pack": {
                        "base_service_api_tag": args.image,
                        "logic_code_uri": f"logic/{api_name}.zip"
                    }
                }

                data = {"metadata_json": json.dumps(metadata)}

                with open(f'{api_name}.zip', 'rb') as file:
                    files = {'aipack_file': (f'{api_name}.zip', file, 'application/zip')}
                    response = requests.post(apilist_url, data=data, files=files, headers=headers)

                    if response.status_code == 200:
                        response_data = response.json()
                        result = (
                            f"Registration Successful!\n"
                            "------------------------------------\n"
                            f"Name: {response_data['name']}\n"
                            f"Creator: {response_data['creator']}\n"
                            f"Created At: {response_data['created_at']}\n"
                            f"Versions: {response_data['versions'][0]['version_num']}\n"
                            "------------------------------------"
                        )
                        print(result)

                        metadata_path = os.path.join(self.settings.workspace, 'metadata.json')
                        with open(metadata_path, 'w') as f:
                            json.dump(metadata, f, indent=4)
                        # 생성된 zip 파일 제거
                        os.remove(f'{api_name}.zip')
                    else:
                        raise Exception(f"Request failed: {response.status_code}, {response.text}")


        elif args.list:
            apilist_url = f"{self.url}/api/v1/workspaces/{workspace_id}/aipacks"
            response = requests.get(apilist_url, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                api_names = [solution['name'] for solution in response_data['solutions']]
                #print(response_data['solutions'])
                title = "API Names"
                box_width = max(len(title), max(len(name) for name in api_names)) + 4

                print(f"┌{'─' * (box_width - 2)}┐")
                print(f"│ {title.center(box_width - 4)} │")
                print(f"├{'─' * (box_width - 2)}┤")
                for api_name in api_names:
                    print(f"│ {api_name.ljust(box_width - 4)} │")
                print(f"└{'─' * (box_width - 2)}┘")
            else:
                print(f"Failed: {response.status_code}, {response.text}")
            return

        elif args.delete:
            ai_pack_name = args.delete

            register_list_url = f"{self.url}/api/v1/workspaces/{workspace_id}/aipacks"
            headers["Content-Type"] = "application/json"
            response = requests.get(register_list_url, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                api_names = {solution['name']: solution['id'] for solution in response_data['solutions']}
                solution_id = api_names.get(ai_pack_name, None)

                if solution_id is None:
                    raise ValueError("Please check service API name!")

                delete_url = f"{self.url}/api/v1/workspaces/{workspace_id}/aipacks/{solution_id}"
                response = requests.delete(delete_url, headers=headers)

                if response.status_code == 200:
                    response_data = response.json()
                    result = (
                        f"Registration Deleted!\n"
                        f"Name: {ai_pack_name}\n"
                        f"Versions: {response_data.get('version_num', 'N/A')}\n"
                    )
                    print(result)
                else:
                    raise Exception(f"Request failed: {response.status_code}, {response.text}")

        else:
            register_apply_uri = f"{self.url}/api/v1/workspaces/{workspace_id}/aipacks"

            api_name = args.name if args.name else input("Service API name: ")
            api_overview = input("Service API description overview: ")
            zip_current_directory(f'{api_name}.zip', exclude_files=['.env', '.token', '.venv'])

            from alm.__version__ import __version__
            metadata = {
                "metadata_version": "1.2",
                "name": api_name,
                "description": {
                    "title": api_name,
                    "alo_version": str(__version__),
                    "contents_name": api_name,
                    "contents_version": "1.0.0",
                    "inference_build_type": "amd64",
                    "overview": api_overview,
                    "detail": [
                        {
                            "title": "title001",
                            "content": "content001"
                        },
                        {
                            "title": "title002",
                            "content": "content002"
                        }
                    ]
                },
                "ai_pack": {
                    "base_service_api_tag": args.image,
                    "logic_code_uri": f"logic/{api_name}.zip"
                }
            }

            data = {"metadata_json": json.dumps(metadata)}

            with open(f'{api_name}.zip', 'rb') as file:
                files = {'aipack_file': (f'{api_name}.zip', file, 'application/zip')}
                response = requests.post(register_apply_uri, data=data, files=files, headers=headers)

                if response.status_code == 200:
                    response_data = response.json()
                    result = (
                        f"Registration Successful!\n"
                        "------------------------------------\n"
                        f"Name: {response_data['name']}\n"
                        f"Creator: {response_data['creator']}\n"
                        f"Created At: {response_data['created_at']}\n"
                        f"Versions: {response_data['versions'][0]['version_num']}\n"
                        "------------------------------------"
                    )
                    print(result)

                    metadata_path = os.path.join(self.settings.workspace, 'metadata.json')
                    with open(metadata_path, 'w') as f:
                        json.dump(metadata, f, indent=4)
                    # 생성된 zip 파일 제거
                    os.remove(f'{api_name}.zip')
                else:
                    raise Exception(f"Request failed: {response.status_code}, {response.text}")


    def deploy(self, args):

        # 최신 버전을 default로 하고 입력으로 받는 경우에만 최신 버전 사용
        workspace_id = self._check_ws(args.workspace)
        token = self._read_token_from_file('access_token')
        headers = {
            "Authorization": f'Bearer {token}',
            "Content-Type": "application/json"
        }
        deployments = "deployments"

        def get_stream_id(stream_list, name):
            for item in stream_list:
                if item['name'] == name:
                    return item['id']
            return None

        # alm deploy list
        if args.list and not any([args.get, args.update, args.delete]):
            deploy_list_url = f"{self.url}/api/v1/workspaces/{workspace_id}/{deployments}"
            response = requests.get(deploy_list_url, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                api_names = [solution['name'] for solution in response_data['streams']]
                title = "Deployed API Names"
                box_width = max(len(title), max(len(name) for name in api_names)) + 4

                print(f"┌{'─' * (box_width - 2)}┐")
                print(f"│ {title.center(box_width - 4)} │")
                print(f"├{'─' * (box_width - 2)}┤")
                for api_name in api_names:
                    print(f"│ {api_name.ljust(box_width - 4)} │")
                print(f"└{'─' * (box_width - 2)}┘")
            else:
                print(f"Failed: {response.status_code}, {response.text}")
            return
            # handle_response(response, 'Deployed API List: ')

        # alm deploy get
        elif args.get and not any([args.list, args.update, args.delete]):
            deploy_get_url = f"{self.url}/api/v1/workspaces/{workspace_id}/{deployments}"
            stream_list = requests.get(deploy_get_url, headers=headers)

            # args.delete 에 지우려는 ai pack name이 있음
            stream_id = get_stream_id(stream_list.json()['streams'], args.delete)
            deploy_get_aipack_url = f"{self.url}/api/v1/workspaces/{workspace_id}/{deployments}/{stream_id}"
            response = requests.get(deploy_get_aipack_url, headers=headers)
            handle_response(response, "Deploy Get Success: ")

        # alm deploy update
        elif args.update and not any([args.list, args.get, args.delete]):
            print("deploy_update hello")

        # alm deploy delete
        elif args.delete and not any([args.list, args.get, args.update]):
            deploy_list_url = f"{self.url}/api/v1/workspaces/{workspace_id}/{deployments}"
            stream_list = requests.get(deploy_list_url, headers=headers)

            stream_id = get_stream_id(stream_list.json()['streams'], args.delete)
            deploy_get_aipack_url = f"{self.url}/api/v1/workspaces/{workspace_id}/{deployments}/{stream_id}"
            response = requests.delete(deploy_get_aipack_url, headers=headers)
            handle_response(response, "Deploy Delete Success: ", keys = ["name"])

        # alm deploy
        else:
            register_list_url = f"{self.url}/api/v1/workspaces/{workspace_id}/aipacks"
            response = requests.get(register_list_url, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                solutions = response_data['solutions']
                solution_id, sol_version_id, solution_version = None, None, None

                # for solution in solutions:
                #     i = 0
                #     if solution['name'] == args.name:
                #         solution_id = solution['id']
                #         print(solution['versions'])
                #         sol_version_id = solution['versions'][i]['id']
                #         if str(solution['versions'][i]['version_num']) == args.version :
                #             solution_version = 'v' + str(solution['versions'][i]['version_num'])
                #             break
                #         i += 1

                for i, solution in enumerate(solutions):
                    if solution['name'] == args.name:
                        solution_id = solution['id']
                        # print(f"Versions for solution {i}: {solution['versions']}")
                        for j, version in enumerate(solution['versions']):
                            sol_version_id = version['id']
                            if args.version == None :
                                solution_version = 'v' + str(solution['versions'][0]['version_num'])
                                break

                            if str(version['version_num']) == args.version:
                                solution_version = 'v' + str(version['version_num'])
                                # print(f"Solution found at index {i}, version found at index {j}")
                                break


                if solution_id is None:
                    raise ValueError("Please check service api name!!")
                
                if solution_version is None :
                    raise ValueError("Please check service api version!!")

                deploy_create_url = f"{self.url}/api/v1/workspaces/{workspace_id}/{deployments}"
                data = {
                    "name": args.name,
                    "version_name": solution_version,
                    "solution_version_id": sol_version_id
                }
                response = requests.post(deploy_create_url, headers=headers, json=data)
                handle_response(response, "Deploy Success: ", keys = ["display_name", "creator","created_at", "updator", "updated_at"])
            else:
                handle_response(response, "Deploy Error: ")

    def activate(self, args):
        workspace_id = self._check_ws(args.workspace)

        # Bearer 토큰이 필요할 경우 헤더에 추가
        token = self._read_token_from_file('access_token')
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        deployments = "deployments"
        # activate list
        if args.list and not any([args.get]):
            deploy_create_url = f"{self.url}/api/v1/workspaces/{workspace_id}/activations"
            # Bearer 토큰이 필요할 경우 헤더에 추가
            response = requests.get(deploy_create_url, headers=headers)
            # todo stream id 찾도록 수정
            # 응답 처리
            if response.status_code == 200:
                response_data = response.json()
                api_names = [solution['display_name'] for solution in response_data['stream_histories']]
                #print(response_data['solutions'])
                title = "Activate API Names"
                box_width = max(len(title), max(len(name) for name in api_names)) + 4

                print(f"┌{'─' * (box_width - 2)}┐")
                print(f"│ {title.center(box_width - 4)} │")
                print(f"├{'─' * (box_width - 2)}┤")
                for api_name in api_names:
                    print(f"│ {api_name.ljust(box_width - 4)} │")
                print(f"└{'─' * (box_width - 2)}┘")
            else:
                print(f"Failed: {response.status_code}, {response.text}")
            return

            # if response.status_code == 200:
            #     data = response.json()
            #     print("Success:", json.dumps(data, indent=4))
            # else:
            #     print("Error:", response.status_code, response.text)

        # activate gets
        elif args.get and not any([args.list]):
            deploy_create_url = f"{self.url}/api/v1/workspaces/{workspace_id}/{deployments}"
            response = requests.get(deploy_create_url, headers=headers)

            # todo stream id 찾도록 수정
            if response.status_code == 200:
                response_data = response.json()
                api_names = [[solution['name'], solution['id']] for solution in response_data['stream']]

                stream_id = None
                for i in range(len(api_names)):
                    if args.service_api_name==api_names[i][0]:
                        stream_id = api_names[i][1]
                if solution_id == None :
                    raise ValueError("Please check service api name !!")

            activate_list_url = f"{self.url}/api/v1/workspaces/{workspace_id}/{deployments}/{stream_id}/activation"

            # POST 요청 보내기
            response_stream_his = requests.get(activate_list_url, headers=headers)
            # 응답 처리
            if response_stream_his.status_code == 200:
                response_stream_hi_data = response_stream_his.json()
                # todo stream_his 구하는 로직 필요

                for streams in response_stream_hi_data['stream_histories']:
                    if streams['status'] == "Running":
                        stream_his_id = streams['id']

                activate_get_url = f"{self.url}/api/v1/activations/{stream_his_id}"
                # POST 요청 보내기
                response = requests.get(activate_get_url, headers=headers)
                # 응답 처리
                if response.status_code == 200:
                    print("Success:", response.json())
                else:
                    print("Error:", response.status_code, response.text)

            else:
                print("Error:", response_stream_his.status_code, response_stream_his.text)
        # activate
        else :
            medatadata_path = os.path.join(self.settings.workspace, 'metadata.json')
            with open(medatadata_path, 'r') as f:
                metadata_dict = json.load(f)
            deploy_create_url = f"{self.url}/api/v1/workspaces/{workspace_id}/{deployments}"
            # Bearer 토큰이 필요할 경우 헤더에 추가
            response = requests.get(deploy_create_url, headers=headers)

            # todo stream id 찾도록 수정
            if response.status_code == 200:
                response_data = response.json()
                api_names = [[solution['name'], solution['id'], solution['solution_version_id']] for solution in response_data['streams']]

                solution_id = None
                stream_id = None
                for i in range(len(api_names)):
                    #print(args.name, api_names[i][0])
                    if args.name==api_names[i][0]:
                        stream_id = api_names[i][1]
                        solution_id = api_names[i][2]
                        # ㅎ해당 내용 찾으면 break
                        break
                if stream_id == None :
                    raise ValueError("Please check service api name !!")
            else :
                print("Error:", response.status_code, response.text)

            activate_url = f"{self.url}/api/v1/workspaces/{workspace_id}/deployments/{stream_id}/activations"
            env_dict = dotenv_values('.env') # type: OrderedDict

            # todo data 구조 확인하기
            streamhistory_info = {
                "stream_history_creation_info" : {
                    "train_resource_name" : "standard",
                    "metadata_json" : metadata_dict,

                },
                "replica": 1,
                "secret" : json.dumps(env_dict)

            }

            # POST 요청 보내기
            response = requests.post(activate_url, headers=headers, json = streamhistory_info)
            # 응답 처리
            if response.status_code == 200:
                handle_response(response, "Activate Success: ", keys = [["stream_history_info", "name"], ["stream_history_info", "creator"], ["stream_history_info", "created_at"], ["stream_history_info", "updator"], ["stream_history_info", "updated_at"], "aipack_activate_url"])
                # print("Success:", response.json())
                self._save_response_json(response)
            else:
                handle_response(response,  "Activate Error: ")
                # print("Error:", response.status_code, response.text)

    def deactivate(self, args):
        workspace_id = self._check_ws(args.workspace)

        # Bearer 토큰이 필요할 경우 헤더에 추가
        token = self._read_token_from_file('access_token')
        #print(f'Successfully authenticated. Token: {token}')
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        deployments = "deployments"

        deploy_create_url = f"{self.url}/api/v1/workspaces/{workspace_id}/{deployments}"
        # Bearer 토큰이 필요할 경우 헤더에 추가
        response = requests.get(deploy_create_url, headers=headers)

        # todo stream id 찾도록 수정
        if response.status_code == 200:
            response_data = response.json()
            api_names = [[stream['name'], stream['id']] for stream in response_data['streams']]

            stream_id = None
            for i in range(len(api_names)):
                if args.name == api_names[i][0]:
                    stream_id = api_names[i][1]
            if stream_id == None :
                raise ValueError("Please check service api name !!")

        else :
            handle_response(response,  "deactivate Error: ")

        activate_list_url = f"{self.url}/api/v1/workspaces/{workspace_id}/{deployments}/{stream_id}/activations"


        # POST 요청 보내기
        response_stream_his = requests.get(activate_list_url, headers=headers)
        # 응답 처리
        if response_stream_his.status_code == 200:
            response_stream_hi_data = response_stream_his.json()
            # todo stream_his 구하는 로직 필요

            stream_his_id = None
            for streams in response_stream_hi_data['stream_histories']:
                if streams['status'] == "Running":
                    stream_his_id = streams['id']
            if stream_his_id is None:
                print("No Running stream history found.")
                return

            activate_delete_url = f"{self.url}/api/v1/workspaces/{workspace_id}/activations/{stream_his_id}"
            # POST 요청 보내기
            response = requests.delete(activate_delete_url, headers=headers)
            # 응답 처리
            if response.status_code == 200:
                handle_response(response, "Delete Success: ", keys = ["display_name", "creator", "created_at", "updator", "updated_at"])
                #print("Success:", response.json())
                try:
                    self._delete_response_json()
                except:
                    print("There is nothing to delete.")
            else:
                print("Error:", response.status_code, response.text)

        else:
            print("Error:", response_stream_his.status_code, response_stream_his.text)

    def get_info(self, args):
        # alm get workspace_info
        # alm get image_info
        # alm get version

        token = self._read_token_from_file('access_token')
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # workspace info
        if args.workspace_info and not any([args.image_info, args.version]):
            workspace_id = self._check_ws(args.workspace_name)

            workspace_info_url = f"{self.url}/api/v1/workspaces/{workspace_id}/info"

            # POST 요청 보내기
            workspace_info = requests.get(workspace_info_url, headers=headers)

            # 응답 처리
            if workspace_info.status_code == 200:
                print("Workspace info:", workspace_info.json())
            else:
                print("Error:", workspace_info.status_code, workspace_info.text)

        # image list
        elif args.image_info and not any([args.workspace_info, args.version]):
            version_rul = f"{self.url}/api/v1/images/info"
            # Bearer 토큰이 필요할 경우 헤더에 추가

            # POST 요청 보내기
            images_list = requests.get(version_rul, headers=headers)

            if images_list.status_code == 200:
                response_data = images_list.json()
                api_names = [solution['tag'] for solution in response_data['images']]
                #print(response_data['solutions'])
                title = "Base image list"
                box_width = max(len(title), max(len(name) for name in api_names)) + 4

                print(f"┌{'─' * (box_width - 2)}┐")
                print(f"│ {title.center(box_width - 4)} │")
                print(f"├{'─' * (box_width - 2)}┤")
                for api_name in api_names:
                    print(f"│ {api_name.ljust(box_width - 4)} │")
                print(f"└{'─' * (box_width - 2)}┘")
            else:
                print(f"Failed: {images_list.status_code}, {images_list.text}")
            return
            # else:
            #     print("Error:", images_list.status_code, images_list.text)

        # version check
        else :
            version_rul = f"{self.url}/api/v1/version"
            # POST 요청 보내기
            aic_version = requests.get(version_rul, headers=headers)
            if aic_version.status_code == 200:
                aic_version = aic_version.json()
                print("AIC Version: ", aic_version['aic']['versions'][0]['ver_str'])
            else:
                print("Error:", aic_version.status_code, aic_version.text)

    def _check_ws(self, workspace_name):
        workspace_name = workspace_name or 'default_ws'
        if workspace_name == 'default_ws':
            workspace_name = self._read_token_from_file('default_ws')
        workspace_id = self._read_token_from_file(workspace_name)  # Read workspace_id from the given or default workspace_name
        return workspace_id

    # error handling 확인
    def _read_token_from_file(self, key_name, file_path='.token/key.json'):
        # 사용자 홈 디렉토리를 가져옴
        home_directory = os.path.expanduser("~")

        # 파일의 전체 경로를 생성
        file_path = os.path.join(home_directory, file_path)

        # JSON 파일에서 토큰 읽기
        try:
            with open(file_path, "r") as token_file:
                data = json.load(token_file)
                access_token = data.get(key_name)
                if access_token is None:
                    raise ValueError(f"입력하신 {key_name}이 존재하지 않습니다.")
                return access_token
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
            return None
        except ValueError as e:
            print(e)
            return None

    def _save_response_json(self, response):
        if isinstance(self.settings.workspace, str):
            data = response.json()
            path = os.path.join(self.settings.workspace, "activate_info.json")
            with open(path, 'w') as f:
                json.dump(data, f)
            print(f"file saved at: {path}")
        else:
            raise TypeError("filepath must be a str")

    def _delete_response_json(self):
        if isinstance(self.settings.workspace, str):
            path = os.path.join(self.settings.workspace, "activate_info.json")
            if os.path.exists(path):
                os.remove(path)
            else:
                print(f"No file found at {path}")
        else:
            raise TypeError("filepath must be a str")

