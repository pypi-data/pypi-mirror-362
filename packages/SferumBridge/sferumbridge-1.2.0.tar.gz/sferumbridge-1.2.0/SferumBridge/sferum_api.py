import requests
from random import randint
import json
from .md import parse_markdown


class SferumAPI:
    def __init__(self, remixdsid):
        """Initializes the SferumAPI instance.

        Args:
            remixdsid (str): User identification cookie used for authorization.
        """
        self.remixdsid = remixdsid
        self.user = None
        self.authorize()

    def authorize(self):
        """Authorizes the user with the provided remixdsid.

        Raises:
            RuntimeError: If request times out or encounters an error.
        """
        try:
            cookies = {"remixdsid": self.remixdsid}
            query = {"act": "web_token", "app_id": 8202606}
            response = requests.get(
                "https://web.vk.me/",
                params=query,
                cookies=cookies,
                allow_redirects=False,
                timeout=3,
            )
            response.raise_for_status()
            self.user = response.json()[1]
            return self.user
        except requests.exceptions.Timeout:
            raise RuntimeError(f"Request to user authorize timed out.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                f"An error occurred during the request to user authorize: {e}"
            )

    def send_message(self, peer_id: int, text: str, reply_to_id: int = None, format: bool = False, **custom_data):
        """Sends a message to a user.

        Args:
            peer_id (int): The recipient's ID.
            text (str): The message text to send.
            reply_to_id (int, optional): The ID of the message to reply to.
            format (bool, optional): Flag indicating if the text should be formatted.
            **custom_data: Additional custom fields to include in the message.

        Returns:
            dict: The response from the API after sending the message.
        """
        url = "method/messages.send?v=5.241"
        data = {
            "access_token": self.user['access_token'],
            "peer_id": peer_id,
            "random_id": -randint(100000000, 999999999),
            "message": text,
        }
        
        for key, value in custom_data.items():
            if isinstance(value, (dict, list)):
                data[key] = json.dumps(value, ensure_ascii=False)
            else:
                data[key] = value
        
        if reply_to_id:
            data['forward'] = "{" + f""" "peer_id":{peer_id},"conversation_message_ids":[{reply_to_id}],"is_reply":true """ + "}"
        
        if format:
            format_list, clean_text = parse_markdown(text)
            data['message'] = clean_text
            data['format_data'] = "{" + f""" "version":1,"items":{json.dumps(format_list)} """ + "}"
        
        return self.request(url, data)

    def delete_message(self, peer_id: int, message_conversation_id: int):
        """Deletes a specific message.

        Args:
            peer_id (int): The ID of the recipient.
            message_conversation_id (int): The ID of the message to delete.

        Returns:
            dict: The response from the API after the request.
        """
        url = "method/messages.delete?v=5.241"
        data = {
            "peer_id": peer_id,
            "cmids": message_conversation_id,
            "delete_for_all": 1,
            "spam": 0,
            "group_id": 0,
            "lang": "ru"
        }
        return self.request(url, data)

    def get_history(self, peer_id: int, count: int, offset: int = 0, start_cmid: int = 99999999):
        """Retrieves the message history for a user.

        Args:
            peer_id (int): The ID of the user whose history to retrieve.
            count (int): The number of messages to retrieve.
            offset (int): The offset to start retrieving messages from.
            start_cmid (int, optional): Conversation message ID to start from.

        Returns:
            dict: The response containing the message history.
        """
        url = "method/messages.getHistory?v=5.241"
        data = {
            "access_token": self.user['access_token'],
            "peer_id": peer_id,
            "start_cmid": start_cmid,
            "count": count,
            "offset": offset,
            "extended": 1,
            "group_id": 0,
            "fwd_extended": 1,
            "lang": "ru",
            "fields": "id,first_name,first_name_gen,first_name_acc,first_name_ins,last_name,last_name_gen,last_name_acc,last_name_ins,sex,has_photo,photo_id,photo_50,photo_100,photo_200,contact_name,occupation,bdate,city,screen_name,online_info,verified,blacklisted,blacklisted_by_me,can_call,can_write_private_message,can_send_friend_request,can_invite_to_chats,friend_status,followers_count,profile_type,contacts,employee_mark,employee_working_state,is_service_account,image_status,photo_base,educational_profile,edu_roles,name,type,members_count,member_status,is_closed,can_message,deactivated,activity,ban_info,is_messages_blocked,can_send_notify,can_post_donut,site,reposts_disabled,description,action_button,menu,role,unread_count,wall",
        }
        return self.request(url, data)

    def get_message(self, peer_id: int, message_conversation_id: int):
        """Retrieves a specific message based on conversation ID.

        Args:
            peer_id (int): The ID of the user.
            message_conversation_id (int): The conversation message ID.

        Returns:
            dict: The response containing the requested message.
        """
        return self.get_history(peer_id, 1, 0, message_conversation_id)

    def execute(self, code: str):
        """Executes a small piece of JavaScript code on the server.

        Args:
            code (str): The JavaScript code to execute.

        Returns:
            dict: The response from the server after executing the code.
        """
        url = "method/execute?v=5.241"
        data = {
            "access_token": self.user['access_token'],
            "code": code,
        }
        return self.request(url, data)

    def request(self, url: str, data: dict):
        """Makes a request to the VK API.

        Args:
            url (str): The API endpoint to call.
            data (dict): The data to send with the request.

        Returns:
            dict: The response from the API.

        Raises:
            RuntimeError: If request times out or encounters an error.
        """
        url = "https://api.vk.me/" + url
        try:
            response = requests.post(url, data=data, timeout=3)
            response = response.json()
            if 'response' in response:
                response = response['response']
                if isinstance(response, dict) and 'items' in response and isinstance(response['items'], list):
                    if all('conversation_message_id' in item for item in response['items']):
                        response['items'] = sorted(response['items'], key=lambda item: item['conversation_message_id'])
            elif 'error' in response:
                match response['error']['error_code']:
                    case 5:
                        self.authorize()
                        data['access_token'] = self.user['access_token']
                        return self.request(url, data)
                    case _:
                        return response['error']

            return response
        except requests.exceptions.Timeout:
            raise RuntimeError(f"Request to {url} timed out.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"An error occurred during the request to {url}: {e}")