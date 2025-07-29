from huggingface_hub import login, HfApi, upload_folder, create_repo


def upload_model(hub_token, directory = "my_model", username = "", repo_name = "", commit_message = "new model created"):
    
    repo_id = f"{username}/{repo_name}"
    
    login(token=hub_token)
    
    create_repo(repo_id)
    
    upload_folder(repo_id = repo_id, folder_path = directory, commit_message= commit_message)
    
    print(f"Model was successfully upload to {repo_id}.")
    