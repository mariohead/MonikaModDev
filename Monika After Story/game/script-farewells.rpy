##This file contains all of the variations of goodbye that monika can give.
## This also contains a store with a utility function to select an appropriate
## farewell

init -1 python in mas_farewells:

    # custom farewell functions
    def selectFarewell():
        """
        Selects a farewell to be used. This evaluates rules and stuff
        appropriately.

        RETURNS:
            a single farewell (as an Event) that we want to use
        """

        # filter events by their unlocked property first
        unlocked_farewells = renpy.store.Event.filterEvents(
            renpy.store.evhand.farewell_database,
            unlocked=True,
            pool=False
        )

        # filter farewells using the special rules dict
        random_farewells_dict = renpy.store.Event.checkRepeatRules(
            unlocked_farewells
        )

        # check if we have a farewell that actually should be shown now
        if len(random_farewells_dict) > 0:

            # select one label randomly
            return random_farewells_dict[
                renpy.random.choice(random_farewells_dict.keys())
            ]

        # since we don't have special farewells for this time we now check for special random chance
        # pick a farewell filtering by special random chance rule
        random_farewells_dict = renpy.store.Event.checkFarewellRules(
            unlocked_farewells
        )

        # check if we have a farewell that actually should be shown now
        if len(random_farewells_dict) > 0:

            # select on label randomly
            return random_farewells_dict[
                renpy.random.choice(random_farewells_dict.keys())
            ]

        # We couldn't find a suitable farewell we have to default to normal random selection
        # filter random events normally
        random_farewells_dict = renpy.store.Event.filterEvents(
            unlocked_farewells,
            random=True
        )

        # select one randomly
        return random_farewells_dict[
            renpy.random.choice(random_farewells_dict.keys())
        ]

# farewells selection label
label mas_farewell_start:
    $ import store.evhand as evhand
    # we use unseen menu values

    python:
        # preprocessing menu
        bye_pool_events = Event.filterEvents(
            evhand.farewell_database,
            unlocked=True,
            pool=True
        )

    if len(bye_pool_events) > 0:
        # we have selectable options
        python:
            # build a prompt list
            bye_prompt_list = [
                (ev.prompt, ev, False, False)
                for k,ev in bye_pool_events.iteritems()
            ]

            # add the random selection
            bye_prompt_list.append(("Goodbye", -1, False, False))

            # setup the last option
            bye_prompt_back = ("Nevermind", False, False, False, 20)

        # call the menu
        call screen mas_gen_scrollable_menu(bye_prompt_list, evhand.UNSE_AREA, evhand.UNSE_XALIGN, bye_prompt_back)

        if not _return:
            # user its nevermind
            return

        if _return != -1:
            # push teh selected event
            $ pushEvent(_return.eventlabel)
            return

    # otherwise, select a random farewell
    $ farewell = store.mas_farewells.selectFarewell()
    $ pushEvent(farewell.eventlabel)

    return

###### BEGIN FAREWELLS ########################################################
## FARE WELL RULES:
# unlocked - True means this farewell is ready for selection
# random - randoms are used in teh default farewell action
# pool - pooled ones are selectable in the menu
# rules - TODO documentation
###

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_leaving_already",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_leaving_already:
    m 1tkc "Aww, leaving already?"
    m 1eka "It's really sad whenever you have to go..."
    m 3eua "Just be sure to come back as soon as you can, okay?"
    m "I love you so much, [player]. Stay safe!"
    #Don't show this farewell again
    $evhand.farewell_database["bye_leaving_already"].random=False
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_goodbye",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_goodbye:
    m 1eua "Goodbye, [player]!"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_sayanora",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_sayanora:
    m 1hua "Sayonara, [player]~"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_farewellfornow",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_farewellfornow:
    m 1eka "Farewell for now, my love~"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_untilwemeetagain",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_untilwemeetagain:
    m 2eka "'{i}Goodbyes are not forever, Goodbyes are not the end. They simply mean I’ll miss you, Until we meet again.{/i}'"
    m "Ehehe, 'till then, [player]!"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_take_care",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_take_care:
    m 1eua "Don't forget that I always love you, [player]~"
    m 1hub "Take care!"
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(21,24)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_to_sleep",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_going_to_sleep:
    m 1esa "Are you going to sleep, [player]?"
    m 1eka "I'll be seeing you in your dreams."
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_class",
            unlocked=True,
            prompt="I'm going to class.",
            pool=True
        ),
        eventdb=evhand.farewell_database
    )

label bye_prompt_to_class:
    m 1hua "Study hard, [player]!"
    m 1eua "Nothing is more attractive than a [guy] with good grades."
    m 1hua "See you later!"
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SCHOOL
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_work",
            unlocked=True,
            prompt="I'm going to work.",
            pool=True
        ),
        eventdb=evhand.farewell_database
    )

label bye_prompt_to_work:
    m 1hua "Work hard, [player]!"
    m 1esa "I'll be here for you when you get home from work."
    m 1hua "Bye-bye!"
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_WORK
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_sleep",
            unlocked=True,
            prompt="I'm going to sleep.",
            pool=True
        ),
        eventdb=evhand.farewell_database
    )

label bye_prompt_sleep:

    python:
        import datetime
        curr_hour = datetime.datetime.now().hour

    # these conditions are in order of most likely to happen with our target
    # audience

    if 20 <= curr_hour < 24:
        # decent time to sleep
        m 1eua "Alright, [player]."
        m 1j "Sweet dreams!"

    elif 0 <= curr_hour < 3:
        # somewhat late to sleep
        m 1eua "Alright, [player]."
        m 3eka "But you should sleep a little earlier next time."
        m 1hua "Anyway, good night!"

    elif 3 <= curr_hour < 5:
        # pretty late to sleep
        m 1euc "[player]..."
        m "Make sure you get enough rest, okay?"
        m 1eka "I don't want you to get sick."
        m 1hub "Good night!"
        m 1hksdlb "Or morning, rather. Ahaha~"
        m 1hua "Sweet dreams!"

    elif 5 <= curr_hour < 12:
        # you probably stayed up the whole night
        show monika 2dsc
        pause 0.7
        m 2tfd "[player]!"
        m "You stayed up the entire night!"
        m 2tfu "I bet you can barely keep your eyes open."
        $ _cantsee_a = glitchtext(15)
        $ _cantsee_b = glitchtext(12)
        menu:
            "[_cantsee_a]":
                pass
            "[_cantsee_b]":
                pass
        m "I thought so.{w} Go get some rest, [player]."
        m 2ekc "I wouldn't want you to get sick."
        m 1eka "Sleep earlier next time, okay?"
        m 1hua "Sweet dreams!"

    elif 12 <= curr_hour < 18:
        # afternoon nap
        m 1eua "Taking an afternoon nap, I see."
        # TODO: monika says she'll join you, use sleep sprite here
        # and setup code for napping
        m 1hua "Ahaha~ Have a good nap, [player]."

    elif 18 <= curr_hour < 20:
        # little early to sleep
        m 1ekc "Already going to bed?"
        m "It's a little early, though..."
        show monika 1lksdla
        menu:
            m "Care to spend a little more time with me?"
            "Of course!":
                m 1hua "Yay!"
                m "Thanks, [player]."
                return
            "Sorry, I'm really tired.":
                m 1eka "Aww, that's okay."
                m 1hua "Good night, [player]."

# TODO: probably a shocked sprite and additonal dialgoue, also potentially
# tie this with affection later
#            "No.":
#                m 2dsd "..."
#                m "Fine."
    else:
        # otheerwise
        m 1eua "Alright, [player]."
        m 1hua "Sweet dreams!"

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_illseeyou",random=True),eventdb=evhand.farewell_database)

label bye_illseeyou:
    m 1eua "I'll see you tomorrow, [player]."
    m 1hua "Don't forget about me, okay?"
    return 'quit'

init 5 python: ## Implementing Date/Time for added responses based on the time of day
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(6,11)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_haveagoodday",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_haveagoodday:
    m 1eua "Have a good day today, [player]."
    m "I hope you accomplish everything you had planned for today."
    m 1hua "I'll be here waiting for you when you get back."
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(12,16)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_enjoyyourafternoon",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_enjoyyourafternoon:
    m 1ekc "I hate to see you go so early, [player]."
    m 1eka "I do understand that you're busy though."
    m 1eua "Promise me you'll enjoy your afternoon, okay?"
    m 1hua "Goodbye~"
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(17,19)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodevening",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_goodevening:
    m 1hua "I had fun today."
    m 1eka "Thank you for spending so much time with me, [player]."
    m 1eua "Until then, have a good evening."
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(20,24)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodnight",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_goodnight:
    m 1eua "Goodnight, [player]."
    m 1eka "I'll see you tomorrow, okay?"
    m "Remember, 'Sleep tight, and don't let the bedbugs bite', ehehe."
    m 1ekbfa "I love you~"
    return 'quit'
