from config import Env


def check_wedding_invite(args: dict, env: Env):
    """
    Check if the query parameters match the expected values for the wedding invite.

    Returns True if all parameters match, False otherwise.
    """

    expected_who = env.wedding_invite_who
    expected_when = env.wedding_invite_when
    expected_where = env.wedding_invite_where
    expected_activity = env.wedding_invite_activity

    return (
        args.get("who") == expected_who and 
        args.get("when") == expected_when and 
        args.get("where") == expected_where and 
        args.get("activity") == expected_activity
    )