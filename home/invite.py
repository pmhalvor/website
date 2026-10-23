from config import Env


def check_wedding_invite(args: dict, env: Env):
    """
    Check if the query parameters match the expected values for the wedding invite.

    Returns True if all parameters match, False otherwise.
    """

    expected_who = (env.wedding_invite_who).upper()
    expected_when = (env.wedding_invite_when).upper()
    expected_where = (env.wedding_invite_where).upper()
    expected_activity = (env.wedding_invite_activity).upper()

    return (
        args.get("who", "").upper() == expected_who and 
        args.get("when", "").upper() == expected_when and 
        args.get("where", "").upper() == expected_where and 
        args.get("activity", "").upper() == expected_activity
    )