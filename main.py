from Classes import Profile


def main():

    profile_list = Profile.get_profile_list()
    for profile in profile_list:
        print(profile)


main()
