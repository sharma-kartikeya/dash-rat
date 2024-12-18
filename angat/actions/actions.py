from ..models.GloveraUser import GloveraUser

def update_user(degree: str, spec: str, college: str, percent: str, backlogs: str, total_exp: str) -> bool:
    try:
        GloveraUser(
            name="Kartikeya Sharma", 
            email='s.kartikeya18@gmail.com', 
            mobile=123,
            bachlors=degree, 
            bachlors_program=spec, 
            univ=college, 
            percentage=percent,
            backlogs=backlogs,
            work_exp=total_exp
        ).save()
        return True
    except Exception as error:
        print(error)
        return False

def chat_with_user(message: str):
    pass

available_actions = {
    "update_user": update_user,
    "chat_with_user": chat_with_user
}