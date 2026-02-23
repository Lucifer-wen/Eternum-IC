# -----------------------------------------
# IncestLables.rpy
# Place redirected label implementations here.
# Register the mapping in IncestMod.rpy under `im_label_map` as
#     "old_label": "new_label",
# Example:
#     In IncestMod.rpy -> im_label_map = { "nancyyogafail": "nancy_yoga_fail_mod", }
#     Here -> define `label nancy_yoga_fail_mod:`
# -----------------------------------------

# Example skeleton (uncomment and adapt):

# Used in annie sister map, replaces a few short lines that would affect other lines and switches a few MC lines to Annie
label welcome_mod:
    play sound carstop fadein 2
    stop musicb fadeout 5
    show welcome 1 with Dissolve(4.5)
    pause 2
    play music2 romantic1
    n "Here we are!" with dissolve
    mc "Wow... the memories..."
    mc "(I still remember this place like it was yesterday...)"
    mc "(Nancy used to pick me up after school and we'd come here.)"
    mc "(Each day I would spend the afternoon playing with her and Dalia. We had dinner every night at eight, and then Nancy drove me home once it got late.)"
    mc "(Now I can't help but feel a little bad for not keeping in contact with them...)"
    mc "(She would always call me on my birthday, but... aside from that, I never reached out. I have to make it up to her somehow.)"
    play sound cardoor
    show welcome 2b with Dissolve(1.5)
    play sound2 cardoor
    show welcome 2
    n "Brings back memories, doesn't it, [mc]?" with dissolve
    show welcome 2b
    mc "It does! It feels like I’m home again."
    show welcome 2
    n "I told you that when you left [mc]... this will always be your home!"
    show welcome 2b
    mc "I know. Thank you, Nancy."
    show welcome 3
    a "WOW... it's so nostalgic!" with Dissolve(1.5)
    n "Do you like it, Annie?"
    a "This place looks awesome! Are you rich?!"
    n "*Laughs* No, I wish. Houses in Kredon are not that expensive."
    a "It's beautiful! I'm used to living in a flat, so this looks like a palace to me!"
    n "My husband and I bought it when I was pregnant with Dalia."
    n "Although he left before she was born, so I was left paying the mortgage all by myself..."
    n "*Clears throat* But that's a story for another day!"
    n "Come on, let's go in quickly before it starts to rain."
    show welcome 4
    n "You first, [mc]!" with Dissolve(1.3)
    a "Rain?"
    show welcome 5
    a "Those don't look like rain clouds to me." with dis
    n "It rains almost every day in Kredon."
    mc "Oh... Now that you’ve mentioned it... Yeah, I guess I do remember the rain."
    n "It's almost a miracle it was sunny today."
    n "Believe me, I've learned to read this sky. It'll start to rain soon."
    a "That's cool! I love rainy days!"
    n "*Laughs* You say that now, but you’ll get tired of them after a while."
    show welcome 4
    n "Alright, let's go! Dalia and Penelope will be inside waiting for us!" with dis
    mc "Can't wait!"
    play sound keys
    stop music2 fadeout 3
    play music2b tictoc fadein 4
    show welcome 6 with Dissolve(2.5)
    play sound2 doorclose
    n "Dalia! Penelope! We're here!" with dissolve
    mc "Hey! You still have that painting you made!"
    a "Did you paint that?!"
    n "Yeah, I used to paint in my free time, but I haven't done anything in years."
    a "It's still impressive!"
    show welcome 7
    mc "Everything looks like it hasn’t changed a bit... Damn, it feels so good to be back." with Dissolve(1.2)
    mc "Is Dalia still the same hyperactive, pigtailed girl that I remember?"
    a "*Laughs* And Penelope the preteen that was too \"cool\" to play with her younger siblings?"
    n "Well... see for yourself!"
    show welcome 8
    n "Dalia! Penelope!!" with hpunch
    n "Come here!"
    play soundlow dooropen3
    p "*Upstairs* Mom!"
    play soundlow doorclose
    d "*Upstairs* Mom?!"
    p "*Upstairs* Finally!"
    d "*Upstairs* She's here!"
    p "*Upstairs* Get out of my way, I'm first!"
    d "*Upstairs* What?! I'm first! Back off!"
    p "*Upstairs* Don't push me!"
    play sound stairsrun
    pause 1.8
    show welcome 9 with dis
    play sound2 slam
    p "I SAID I'M FIRST!" with hpunch
    d "SCREW YOU!"
    show welcome 10
    n "Wow, girls!" with Dissolve(1.2)
    n "I wasn't expecting you to be so excited to meet [mc] again!"
    d "Huh?"
    play music2 happy3 fadein 3
    stop music2b fadeout 5
    show daliapen_presentation with Dissolve(1.3)
    pause 3.2
    show pendaliap2
    pause 1
    $ daliau = True
    $ penelopeu = True
    p "Who?" with dissolve
    hide daliapen_presentation
    d "[mc]?"
    play soundlow whoosh3
    show pendaliap
    p "Oh... O-Of course! [mc]!"
    d "Oh, y-yeah, so excited! Hi [mc]!"
    p "It's been a while!"
    d "Yeah, welcome back!"
    mc "Thanks!"
    a "So good to see you, sis!"
    d "Same here!"
    p "Yes! So good!"
    mc "Yeah!"
    d "Good!"
    p "Good, yeah!"
    d "Good..."
    play soundlow whoosh3
    show wipe2
    p "Okay, Mom, I need to ask for a favor!"
    p "PLEASE!"
    hide pendaliap
    hide wipe2
    hide pendaliap2
    show welcome 14
    d "Mom! Listen to me first! It's urgent!"
    show welcome 12
    p "That can wait! I need help!"
    show welcome 13
    n "*Sighs*" with dissolve
    n "What happened now?"
    show welcome 12
    p "I need the car! Just for a couple of hours! My entire career depends on it!"
    show welcome 14
    d "I need my running shoes! I can't find them! They say it's going to rain in half an hour!"
    show welcome 15
    n "Both of those things can wait! You didn't even welcome [mc] and Annie properly!"
    n "They're gonna live with us for a whole year. You know that, right?"
    show welcome 12
    p "But we just did!"
    show welcome 13b
    p "[mc]! I can't wait to properly meet you!" with dis
    p "I wish I could stay, but I really need to go!"
    show welcome 13a
    p "Oh, and you must be Annie! Nice to meet you too!"
    a "Thank you!"
    d "Welcome to the family!"
    d "By the way, I love your haircut!"
    a "*Giggles* Thank you so much!"
    show welcome 13c
    d "Damn [mc], you look... tall!"
    mc "Thanks, Dalia. You look... tall too."
    mc "Taller than you used to be, at least."
    d "I'm sure we'll have so much fun later reminiscing about the old days, but I have to complete my training now."
    d "Y-You don't mind, do you?"
    d "PLEASE?!"
    show welcome 13b
    p "Of course he doesn't mind!"
    p "You wouldn't want to destroy my career, right?"
    p "RIGHT?!"
    default conver1 = False
    menu:
        with dis
        "Ask them to stay":
            mc "Well, I was expecting you to stay and hang out today..." with dis
            mc "Come on, I'm sure your other plans can wait."
            show welcome 13bbb
            p "Ugh..." with dis
            p "Thank you for your help, [mc]."
            p "I can see you're a cool one, jeez..."
            show welcome 12
            p "Don't listen to him, Mom!" with dis
        "Ask for a favor in return":
            mc "Well, maybe if you do me a simple favor later, I won’t mind you leaving..." with dis
            show welcome 13bbb
            p "Um... excuse me?" with dis
            p "A favor?"
            p "Do you think we're making a deal or something?"
            p "I was asking for support, not permission."
            p "I can see you're a cool one, jeez..."
            show welcome 12
            p "Don't listen to him, Mom!" with dis
        "{color=[walk_points]}Let them go [pink][mt](Penelope, Dalia +1)":
            mc "Sure, no worries. I was going to sleep early anyway." with dis
            mc "We can talk tomorrow!"
            $ conver1 = True
            $ penelope_points += 1
            $ dalia_points += 1
            play sound "beat.ogg"
            show welcome 13bb
            show heartr at topleft
            with dis
            hide heartr
            p "See?!" with dissolve
            p "Even [mc] is asking you to let us go!"
            show welcome 13c
            d "Because he's cool! It's good to see the city didn't change you, [mc]." with dis
    show welcome 13
    n "*Sighs* What do you need the car for?" with dis
    show welcome 16
    p "Gucci is doing a casting call for female models at the mall!" with dis
    p "This is the opportunity I've been waiting for!"
    p "My chance to become a professional model!"
    p "To finally make my dreams come true!"
    show welcome 12
    p "Please, Mom!" with dis
    show welcome 13
    n "Hmm... And they’re only doing it today?"
    show welcome 12
    p "Yes!"
    show welcome 13
    n "And you won’t have to wear anything risque right? Won’t be wearing only your underwear or something crazy?"
    show welcome 12
    p "Of course not! What do you take me for?"
    n "Hmm..."
    show welcome 13
    n "Okay, okay, take the keys..."
    n "But I want you home before 10."
    n "And don't talk to any strangers outside of the casting call!"
    show welcome 12
    p "Mom! I'm not 10 years old anymore!"
    show welcome 16
    p "But thank you! I'll be right back, I promise!" with dis
    p "Bye!"
    show welcome 17 with dis
    play sound doorclose
    n "Well then, what's the matter with you?" with dissolve
    d "Where are my running shoes?! The ones that can get wet!"
    n "They're next to the garage door, but you're not going anywhere."
    d "Mom!! You can't do this to me!"
    d "I need to run 10 miles every day or I'll stay behind!"
    d "The gym's annual competition is just two weeks away!"
    n "So what's the big deal? You're already one of the best athletes in town!"
    show welcome 18
    d "But not the best. That damn Micaela always lifts more weight than I do!" with dis
    d "I can't beat her at that, but I can beat her at the run if I train every day. Perhaps in squats too."
    d "If I skip a single training day, she could humiliate me again like last year. I'm not gonna let that happen."
    show welcome 17
    d "Please, Mom!" with dis
    n "Okay, okay... you can go, but same as your sister: I want you home before 10."
    d "Yes! I won’t be a minute late!"
    d "Thanks Mom, you're the best!"
    d "Love ya!"
    show welcome 19 with Dissolve(1.5)
    play sound doorclose
    n "*Sighs*" with dissolve
    n "What am I gonna do with these two..."
    show welcome 20
    n "I'm so sorry guys, this is not what I wanted to happen..." with dis
    mc "Don't worry about it, Nancy!"
    if conver1:
        mc "As I said, I think I'm going to sleep very early today."
    n "Annie, you must have gotten the wrong impression of my daughters..."
    show welcome 21
    a "Not at all! They both seem really nice!"
    a "For tonight, I’d rather just unpack all my things and freshen up a bit. We have plenty of time to get to know each other in the days to come!"
    show welcome 24b
    n "You're so nice, Annie. Is there anything I can do for you?"
    show welcome 21
    a "Well, since you asked... What's the WiFi password?"
    show welcome 22
    mc "Ah... still planning to log into Eternum?" with dis
    a "*Giggles* I’m just going to check to make sure everything is still working..."
    mc "Sure..."
    show welcome 24b
    n "Oh, you play Eternum too?"
    n "Dalia is really hooked on that game."
    show welcome 23
    a "REALLY?!" with hpunch
    show welcome 24
    a "Oh boy, this is great news!" with dis
    show welcome 24b
    n "Sometimes I think Dalia does nothing all day except play Eternum and go to the gym."
    n "Maybe you can play together sometime."
    show welcome 24
    a "Of course!"
    a "I'll invite her to my favorite server: Ion!"
    a "Wait! No! Plains of Denaria!"
    a "No, no! Xala's Moon!"
    show welcome 26
    mc "*Yawns* Well, I think I'm off to bed." with dis
    show welcome 25
    n "What?!" with dissolve
    n "Without any supper?"
    mc "Yeah..."
    mc "I'm sorry, I’m having a hard time keeping my eyes open."
    mc "I couldn't sleep on the plane, nor on the train ride from the airport."
    show welcome 26
    n "It's okay honey, I understand. Of course you can go to sleep." with dis
    n "Your room will be on the second floor—the last one on the right."
    mc "Ah, I remember that room! It was the one with a lot of natural light."
    n "That’s the one! So please, make yourself at home!"
    show welcome 24b
    n "Well, since [mc] seems to remember where everything is already... Do you want a tour of the house, Annie?"with dis
    show welcome 24
    a "I'd love that!"
    mc "Okay! I'll leave you two alone! Good night, girls."
    show welcome 22
    a "Goodnight [mc]! Sweet dreams!" with dis
    show welcome 26
    n "Tomorrow is your first day at your new school, so it's probably a good idea to get a good night’s rest."
    n "Goodnight, [mc]."
    mc "See you tomorrow!"
    jump dream1

# Used in base map, adds a few flavor lines
label daliacove_mod:
    stop music fadeout 6
    show black with Dissolve(2.2)
    pause
    show screen afewhourslater with dis17
    pause
    if tellpassword:
        play music2 party fadein 7
        hide screen afewhourslater
        scene cd 1
        with Dissolve(2.2)
        pause
        gymm "Blake! Beer me, dude!"with dis08
        gymm2 "Here you go! Cold and bubbly!"
        gymm "Thanks, bro."
        mc "Holy shit!"
        show cd 0
        mc "(Look at this!)" with dis12
        mc "(I wasn't expecting a whole beach party here! I guess that’s one way for Dalia to get over the competition.)"
        mc "(From what she told me, I assumed it was gonna be a quiet cove.)"
        mc "(There's a pretty good vibe here, though.)"
        show cd 0b
        mc "Well, well, well..."with dis12
        mc "What do we have here?"
        mc "You forgot to tell me that you threw parties in your \"private\" server, didn't you?"
        d ". . ."
        mc "Hello? Earth to Dalia."
        show cd 0c
        d ". . ." with dissolve
        mc "Hey, I won't complain, though. It's a really nice setup you have here."
        mc "Who are all these people, though? Friends from...?"
        d ". . ."
        mc "Cat got your tongue or what?"
        bro "Welcome to the party!"
        show cd 0f
        mc "*Turning around* Huh?"with dis
        mc "What? What the fuck are you doing here? Did you seriously invite him too?"
        show cd 0g
        bro "I'm the one who's throwing the party."
        bro "But don't worry, I'll let you stay."
        if punchbrock:
            show cd 0h
            bro "That fucking punch of yours still hurts even in Eternum, not gonna lie..." with dis
            show cd 0g
            bro "But no worries bro, I don't hold grudges. It was just a lucky hit, anyway..." with dis
        show cd 0f
        mc "What are you talking about? Do you know the password too?"
        show cd 0g
        bro "Of course I do. You told me yourself."
        show cd 0f
        mc "What? No, I didn't."
        show cd 0g
        bro "Of course you did. Don't you remember? In the fitness room, with that friend of yours with that shirt of Micaela."
        show cd 0f
        mc "What?! You were eavesdropping on us?! You're a fucking asshole!"
        mc "That was private!"
        show cd 0g
        bro "It's not as if you were whispering, bro."
        bro "Having a private server in Eternum and not sharing it is a very selfish thing, after all. I thought you were inviting everyone in the gym to come."
        bro "Now it's so much more fun!"
        show cd 0f
        mc "(Fucking idiot...)"
        show cd 0c
        mc "*Turning around* O-Okay, I can explain."with dis
        bro "Yo guys, let's turn up that music! I want all of Eternum to hear us!"with hpunch
        mc "I didn't tell him, I swear!"
        mc "But he was spying on me when..."
        show cd 0d
        d ". . ." with dis12
        d "Don't talk to me ever again."

        # CCMOD: ACHIEVEMENT: Oathbreaker
        if renpy.loadable("achievements/achievements.rpy"):
            $ award_by_name("Oathbreaker")

        mc "W-What?"
        show cd 0e with dis
        mc "Dalia!" with dis08
        mc "Oh... FUCK!"
        mc "(I really screwed the pooch this time...)"
        show cd 1
        mc "*Sighs* (I guess I'll just log off for today...)"with dis15
        mc "(She seemed really upset...)"
        mc "(And to be fair, she has reasons to be.)"
        mc "(Anyway... I'll apologize after she cools off. This is just the bathtub thing all over again.)"
        mc "(Tomorrow's another day...)"
        $ daliapath = False
        $ daliau = False

        # CCMOD: ACHIEVEMENT: Jerry's Big Chance
        if renpy.loadable("achievements/achievements.rpy"):
            $ award_by_name("Jerry's Big Chance")

        jump nightmare04
    play musicb waves2 fadein 7
    hide screen afewhourslater
    scene cd 1
    with Dissolve(2.5)
    pause
    show cd 2 with dis2
    pause
    d ". . ."with dis08
    show cd 3
    d "(Today the sea is very calm.)"with dis15
    d "(I wish it was always like this... It almost looks like a pool.)"
    d ". . ."
    d "*Sighs*"
    d "(I'm pathetic.)"
    show cd 4 with dis17
    pause
    play sound sand
    stop musicb fadeout 15
    play music2 cove fadein 5
    show cd 5 with dis15
    pause .2
    mc "Did you know that sex is a death sentence for octopuses?" with dis
    mc "After the mating is done, it's game over for both of them."
    show cd 6
    mc "The male wanders off to die, and the female guards their eggs so obsessively that she even stops eating."with dis
    mc "When the eggs hatch, her body undergoes a cascade of cellular suicide until she dies as well."
    mc "Quite a sad fate, huh? Nature sure can be cruel."
    d ". . ."
    show cd 8
    d "How did you know where I would be?"with dis08
    show cd 7
    mc "Well, you told me yourself that you liked to come here when you wanted to relax or be alone."
    mc "I assumed I'd find you here."
    show cd 8
    d "When I told you the password, you said that you wouldn't come here without asking for my permission first."
    show cd 7
    mc "That’s true. Guilty as charged!"
    mc "I just thought that... after what happened, you'd like to have some company."
    show cd 8
    d "I don't wanna talk about it."
    show cd 7
    mc "No one's forcing you to!"
    mc "I was just telling you some awesome trivia about the fascinating world of octopuses. Technically, it was you who interrupted me and my fun facts."
    show cd 9
    d "*Snorts*" with dis04
    show cd 10
    d "True. I'm sorry."
    d "Please continue. Enlighten me."
    show cd 9
    mc "Thank you."
    mc "You see... although it's commonly said that they have 8 legs, in fact they have 6 arms and 2 legs."
    mc "If they are desperately hungry, they can eat their own arms, which will grow again after some time."
    mc "They have 3 hearts, and their blood is blue!"
    show cd 10
    d "Oh, so they're true blue royalty, huh?"
    show cd 9
    mc "Exactly!"
    mc "Not to mention, they're also said to be the most intelligent animal of all invertebrates."
    mc "They say that if octopuses had longer life spans, they would be the dominant species in the world."
    show cd 10
    d "Wow, that's scary."
    show cd 9
    mc "Right? We'd better be on the watch. You never know when they could attack... Plus, you ever see all that tentacle porn online? That shit’s not something to mess around with."
    show cd 10
    d "*Laughs* How the hell do you know all this stuff?"
    show cd 9
    mc "I've always liked the sea and marine life."
    mc "Do you remember when we went to the Aquarium?"
    mc "When we were like... 7?"
    show cd 10
    d "I do!"
    d "Mom took us there for my birthday."
    if divinationflashback:
        d "I remember seeing the sharks and thinking..."
        show cd 6
        mc "\"{i}One day I'll have my own boat! {/i}\""with dis12
        mc "\"{i}I'll navigate the seven seas and discover all the sea monsters that are hiding across the world! {/i}\""
        mc "\"{i}I'm Dalia the Explorer! {/i}\""
        show cd 11
        d "H-How do you remember that?" with dis12
        d "I thought you said you barely remembered your time in Kredon..."
        show cd 12
        mc "I was playing with Penny and Luna the other day and we used a device that dug up some old memories."
        mc "*Chuckles* And it's hard to forget your \"Dalia the Explorer\" phase."
    else:
        d "I remember seeing the sharks and thinking that one day I'd explore the seven seas with my own boat."
        show cd 9
        mc "I do remember your \"Dalia the Explorer\" phase!"
    mc "You kept repeating it all the time."
    show cd 10
    d "*Sighs* Yeah..." with dis04
    d "That was fun."
    d "I miss those carefree days when my only concern was what Mom would give us for dinner."
    show cd 9
    mc "*Chuckles* If it had been up to me, I'd have only eaten candy and potato chips all day."
    mc "Good thing that’s changed."
    show cd 10
    d "Yeah..."
    show cd 14
    d "Look, [mc]..." with dis12
    d "I appreciate you coming here. I really do."
    d "But... you can go now, don't worry about me."
    d "I mean, I know what you're thinking."
    d "\"This drama queen’s overreacting to a stupid competition that has 0 real-world value.\""
    d "\"If she'd had any {i}real{/i} problems during her lifetime, she wouldn't be crying over something so trivial.\""
    d "\"What a spoiled little girl.\""
    show cd 15
    mc "Wow, everything you just said was wrong."with dis12
    mc "I wasn't thinking that at all. I thought you knew me better than that, Dalia."
    mc "That competition was important to you, and that's all that matters."
    mc "I've been hearing you waking up at 5 AM every morning to go train."
    mc "I've seen your folders full of different gym programs."
    mc "I've even seen your sneakers’ soles get completely worn down and reduced to shreds from overuse."
    mc "No one likes to lose. After so much effort, I'd be pissed too."
    mc "It's totally normal."
    show cd 14
    d "It's..." with dis
    d "It's not even about the damn competition."
    d "It's just that... being good at sports is the one thing I have."
    d "I'm not funny. I'm not particularly clever or cunning, like Mom. I don’t have Penny’s supermodel-tier looks. I don't have any talent for music or art... I'm average at everything."
    d "The one thing I had was being... \"the fit girl.\""
    d "And if I can't even get that right..."
    d "Then I'm nothing."
    show cd 13
    mc "(Damn, I didn't know Dalia was so insecure deep down.)"
    mc "(It hurts to see her like this.)"
    show cd 15
    mc "You're unique and special, Dalia. You don't have to be the best at something to be somebody."with dis
    mc "Look at me! I'm the most average dude you'll ever see! I don't have any real talent, and yet, here I am."
    show cd 14
    d "That's not true."with dis
    d "You're a lot smarter than me. You got offered a full scholarship to participate in Kredon’s student exchange program."
    d "You started playing Eternum a few weeks ago, and you already managed to surpass me and learn a secret magic no one knows anything about."
    d "You're special..."
    play sound sand
    show cd 16
    d "And I'm not." with dis12
    d "Let’s just stop arguing about it and accept it."
    d "Acknowledging and accepting it are the first steps t–"
    play sound snow2
    show cd 17
    mc "*Getting on top of her* Okay, that's enough!"with dis08
    d "W-What are you doing?!"
    show cd 18
    mc "You're done talking nonsense for today."with dis
    mc "You're amazing, Dalia. Everything about you is amazing. And we're not leaving this beach until you accept it."
    show cd 19
    d "Okay, okay..."with dis04
    show cd 18
    mc "No, not okay. I want you to say it out loud."with dis04
    mc "\"I'm amazing.\""
    show cd 19
    d "Oh come on, what are we, 5?"with dis04
    d "Don't make me do it."
    show cd 18
    mc "I don't know about you, but I can stay here all day. This pose is quite comfortable."with dis04
    show cd 19
    d "You're kinda crushing my stomach."with dis04
    show cd 18
    mc "More reason to do what I say, then."with dis04
    show cd 19
    d "*Sighs* What the hell do you want?"with dis04
    show cd 18
    mc "\"I'm amazing.\""with dis04
    show cd 19
    d "*Sighs*"with dis08
    d "{size=25}I'm amazing..."
    show cd 18
    mc "Yes, you are."with dis08
    mc "You're funny, you're generous and kind, and you're the strongest girl I know."
    mc "You're one of my favorite people to spend time with, and one of the sexiest women I've ever met."
    mc "Your face looks beautiful at any time of the day, and you have an absolutely killer body."
    mc "Oh..."
    mc "And you're a pretty good kisser too."
    play sound snow2
    show cd 20
    d "*Snorts* Shut up! Haha!"with dis
    d "Don't remind me of that!"
    show cd 22

    # CCMOD: PHONE
    if renpy.loadable("achievements/achievements.rpy"):
        $ unlock_wallpaper_by_name("wp_dalia_4")

    mc "*Chuckles* Hey, it's true!" with dis15
    show cd 21
    d "*Chuckles* That was so embarrassing! I don't know what got into me. God, did you see the looks on their faces?"
    d "I wish the ground swallowed me up at that moment!"
    show cd 22
    mc "Hey, I actually thought..."
    mc "It was a good kiss."
    show cd 21
    d "Yeah, I guess it was..."
    show cd 24
    d "Thank you [mc]."with dis12
    show cd 23
    mc "For what?"with dis04
    show cd 24
    d "Talking to you made me feel better."with dis04
    d "It always does..."
    d "I guess you can add that to the list of your many talents."
    show cd 23
    mc "I have far too many talents. I’m gonna have to start carrying a list around."with dis04
    show cd 24
    d "*Chuckles* Oh, really?! Now you're showing your true colors!"with dis04
    d "Your humbleness from before was all a facade, wasn't it? “I’m the most average dude you’ll ever see.” You liar!"
    show cd 23
    mc "Oh yeah, totally. Now that you’ve accepted that you're amazing too, I don't have to pretend anymore."with dis04
    mc "I'm pretty damn awesome, let's be honest."
    show cd 24
    d "*Laughs* Fuck off."with dis04
    show cd 23
    mc "*Laughs*"with dis04
    show cd 1 with dis2
    stop music2 fadeout 9
    play music waves2 fadein 10
    d "Well, I guess we should get going now." with dissolve
    d "I think it's pretty late."
    if punchbrock and daliabet:
        mc "Oh, before we leave, I wanted to ask you something..."
    else:
        mc "Yeah, I guess it is."
        mc "I'm really hungry."
        d "I hope you are, because I'm making dinner tonight. And I'm serving Dalia-sized portions!"
        mc "Nice!"
        $ daliapath = False
        $ daliau = False

        # CCMOD: ACHIEVEMENT: Jerry's Big Chance
        if renpy.loadable("achievements/achievements.rpy"):
            $ award_by_name("Jerry's Big Chance")

        jump nightmare04
    mc "Do you remember our bet in the Semper Invicta server?"
    show cd 27
    d "Oh man, hold your horses bud!" with dis15
    d "Don't you try to take advantage of this situation!"
    d "Thanks to you I'm not feeling down anymore, so you won't be able to have your way with me in a moment of weakness, sorry."
    show cd 26
    mc "Oh I know, that's why I'm bringing it up."
    show cd 28
    d "Look, I'm very tired, and my shorts are full of sand, so I'm not in the mood to fight with you right now."
    d "Maybe... another day."
    show cd 26
    mc "You should get rid of the sand if it’s making you uncomfortable."
    show cd 27
    d "I’m not gonna fight you, [mc]."
    d "Our... \"bet\" will have to wait."
    show cd 26
    mc "I know! I just want to tell you something. Trust me, you're gonna love it."
    show cd 27
    d "Why are you so pushy? You don't have a chance against me anyway."
    show cd 26
    mc "Ahhh, it's nice to see you regaining self-confidence."
    d ". . ."
    show cd 29
    d "What are you concocting in that pervy little brain of yours?" with dis12
    mc "I'm innocent, I swear."
    d "Of course..."
    show cd 30
    d "Fine, fine, let me “get comfortable.”"with Dissolve(1.3)
    d "It was a bad idea to sit down on the sand with pants on, anyway."
    mc "That's exactly what I'm saying."
    play sound clothes3
    show cd 31 with dis15
    $ unlock_look("dalia", 9)
    mc "(Jesus...)" with dissolve
    show cd 32
    mc "This bikini looks good on you, Dalia." with dis
    d "Thanks. I knew I liked it beforehand because I have the exact same model in the real world, so I bought it here as well."
    mc "You’re definitely looking more comfortable now."
    d "Oh, for sure..."
    play sound sand
    show cd 33 with dis15
    mc "(Oh my fucking god, those hips...)"with dissolve
    # ===== new stuff =====
    if nancy03scene:
            mc "(Those abs... is it bad that I want to lick them? Well, after what happened with Mom...)"
    else:
            mc "(Those abs... is it bad that I want to lick them?)"
    # ===== end new stuff =====
    show cd 34
    d "Okay, so... what did you want to tell me? I'm all ears."
    show cd 33
    mc "Ah, yeah."
    mc "Y’know that asshole from the gym, Brock? The guy you unjustly lost to?"
    d "Mm-hm."
    mc "After you left, we had a little argument, he provoked me, and..."
    mc "I might have punched him in the face."
    mc "Maybe a bit too hard."
    show cd 34
    d "*Snorts* Seriously?"
    show cd 33
    mc "Yeah. I think he fell unconscious."
    show cd 34
    d "Hah! Serves him right. Nice one!"
    show cd 33
    mc "Yeah, the guy was a total idiot."
    show cd 34
    d "Definitely."
    d "But... I fail to see the connection between this and our bet, though."
    show cd 33
    mc "Well, that's the thing... {i}Technically{/i}, you lost against him in combat."
    mc "And {i}technically{/i}, I beat him shortly after."
    mc "Therefore, by the transitive property, I beat you too."
    show cd 34
    d "*Chuckles* Excuse me? That's not how it works at all."
    show cd 33
    mc "I'm pretty sure it's valid. We didn't specify the rules."
    show cd 34
    d "Yeah, we didn't, but it's common sense."
    d "If I had made out with my sister yesterday, does that mean you could say that you’ve kissed Penelope too?"
    show cd 33
    mc "You made out with Penelope yesterday?!"
    show cd 34
    d "*Laughs* Of course not! I'm just trying to show the flaw in your logic."
    show cd 33
    mc "Okay, okay... whatever you say..."
    mc "*Chuckles* It was worth a try, though."
    mc "I was hoping I didn't have to punch that pretty face of yours in order to win, but I guess I'll have to do it. You’ve left me no choice."
    mc "Unless you find another technicality, of course..."
    show cd 34
    d "You're the one who's trying to find loopholes in our bet."
    show cd 33
    mc "*Chuckles* That depends on how you look at it."
    mc "Anyway, let's go home."
    mc "I loved spending some time with you in your server, Dalia. Thanks for letting me visit."
    d ". . ."
    # ===== new stuff =====
    d "{size=15}Fuck it"
    mc "What did you say?"
    show cd 34
    d "I said okay... let's do it."
    # ===== end new stuff =====
    show cd 33
    mc "The Exit Portal inside the cave is the only one around? Have you ever explored the rest of the island?"
    show cd 34
    d "I'm talking about the bet. Let's do it."
    show cd 33
    mc "The..."
    $ renpy.music.set_volume(0.4, channel='music3')
    play music3 covesexy fadein 8
    stop music fadeout 10
    mc "W-Wait, what?"
    show cd 34
    d "Isn't that what you wanted?"
    show cd 33
    mc "Um... y-yeah..."
    play sound sand
    show cd 35
    d "*Undoing her bikini* Never let it be said that Dalia doesn't honor her bets." with dis12
    if not rotundafail:
        d "The other day I bet and won 100 eternals in the rotunda from Jasticus' trainer."
    d "Sometimes you win, sometimes you lose..."
    play sound2 sand
    show cd 36
    mc "*Standing up* Did this really work? Or am I dreaming?"with dis12
    show cd 37
    d "Everything you did for me today really meant a lot. Coming to the competition, giving me that pep-talk before the trials, cheering me on and cheering me up..."with dis04
    d "You came looking for me when I was at one of my lowest points, and you helped me regain my self-esteem."
    d "And... well, that kiss honestly wasn’t half bad."
    d "So... as a thank you for everything... I'm choosing not to overthink your definition of \"beating me in a fight.\""
    show cd 38 with dis17
    mc "My god..." with dis08
    mc "You're fucking perfect..."
    show cd 39
    d "You’re saying so many nice things today... but well, I can't say I don't like being praised..."with dis04
    play sound sand
    show cd 40
    if dalianaked:
        d "I know you already saw me naked, but I hope this can still get you in the mood." with dis12
    else:
        d "Well... I hope this is enough to get you in the mood."with dis12
    d "It's gonna be difficult to do my part otherwise."
    show cd 41

    # CCMOD: PHONE
    if renpy.loadable("achievements/achievements.rpy"):
        $ unlock_wallpaper_by_name("wp_lewd_dalia_1")

    mc "I doubt that'll be a problem..."
    if dalianaked:
        show cd 40
        d "At least this time I'm getting naked for you voluntarily, not accidentally. You creep."
        show cd 41
        mc "I thought it was clear that that was just a huge misunderstanding..."
        show cd 40
        d "*Giggles* I still have my doubts..."
    show cd 42 with dis15
    d "*Starts to slowly open your fly*"with dis08
    # ===== new stuff =====
    if nancy03scene:
            mc "(Oh... fuck yeah! Screw it! No matter if she's my sister, I already did it with my mom, so this can't be any worse.)"
    else:
            mc "(Oh... fuck yeah! My sister’s gonna give me a blowjob!)"
    # ===== end new stuff =====
    play sound zip
    pause .2
    play sound2 clothes3
    show cd 43 with dis17
    d "What the..." with dissolve
    d "Jesus Christ..."
    d "I wasn't expecting..."
    d "T-That..."
    show cd 44
    mc "*Taking off your shorts* I mean..."with dis15
    play sound clothes3
    show cd 45
    mc "You made me so fucking horny, Dalia. Do you see how hard you made me?"with dis12
    mc "I’m like a rock. Couldn't help it. Your tits, your ass, your abs... the entire package."
    show cd 46
    d "Still, that was way too fast. Did you get hard during our sincere and emotional exchange?"with dis04
    show cd 45
    mc "Of course not... only once you took off your pants. Your tummy is way too sexy."with dis04
    show cd 46
    d "I'll choose to believe you..."with dis04
    d "I don't want to dirty our best memory together."
    show cd 45
    mc "Dirty the memory? We're only making it better..."with dis04
    show cd 46
    d "Yeah, I’m sure we’re making it better for you."with dis04
    d "Anyways..."
    d "I should probably start before this... monster starts going down."
    show cd 45
    mc "I don't think that's gonna happen..."with dis04
    mc "Take your time... I’m not in a rush."
    show cd 47
    d "*Gets close to you*" with dis15
    mc "(Oh fuck yeah...)"
    d "(Jesus, this thing looks huge up close... and the smell...)"
    show cd 48
    mc "You sure you can take it?" with dis
    show cd 49
    d "Of course."
    show cd 48
    mc "Is it making you horny?"
    show cd 49
    d "N-no!"
    show cd 48
    mc "You're in denial today, Dalia..."
    show cd 50
    d "I'm already starting to regret agreeing to this."with dissolve
    mc "Your mouth says that, but your eyes say otherwise..."
    d "Shut up, idiot."
    show cd 51
    blank "{i}She starts licking the head of your penis."with dis12
    mc "Oh, yeah..."
    show cd 52
    blank "{i}Gently kisses and licks you along the length of your cock."with dis12
    show cd 51
    mc "(I can feel how her breathing keeps speeding up...)"with dis12
    show cd 52
    mc "You're driving me insane, Dalia..." with dis12
    mc "Stop teasing me... Put it inside your mouth, please..."
    d "I thought you said you weren’t in a rush..."
    show cd 51
    mc "I might have spoken too soon..."with dis12
    show cd 53 with dis12
    mc "Oh, y-yes..." with dissolve
    show cd 51
    d "Does it feel good?" with dis12
    show cd 53
    mc "It feels amazing..." with dis12
    show cd 54
    d "*Slight moan*"with dis12
    mc "Oh fuck yeah, baby..."
    show cd 55
    mc "(Oh my god, Dalia's sucking my cock...)"with dis12
    mc "(This is like a dream come true...)"
    show cd 56
    mc "Oh... fuck, your mouth is so warm..." with dis12
    mc "That’s a good girl..."
    show cd 57
    mc "(God, I'm stretching her little mouth so much...)"with dis
    show cd 56
    mc "That's it, Dalia..."with dis
    mc "Deeper..."
    show cd 57
    mc "Make it wet..."with dis
    show cd 58
    mc "Now, let's try that ability of yours we talked about all those weeks ago, shall we?" with dis12
    d "Mmmm...?"
    play sound blow4
    play sound2 blow4
    show cd 59
    blank "{i}You gently push Dalia's head further onto your cock."with dis12
    d "Mmmph!"
    mc "Oh f-fuck, yes!"
    play sound3 blow5
    show cd 60
    d "*Recovering her breath* AAahh..." with dis12
    mc "Holy shit, so it was true, huh? No gag reflex..."
    d "*Panting* I m-might have underestimated the size..."
    mc "Is it too much for you?"
    d "*Panting* Of course not, but..."
    d "W-Well, I s-still have to breathe, you know?"
    d "Are you trying to kill me?"
    mc "Not at all..."
    mc "I'll let you set the pace... Be as greedy as you want."
    scene cd 56
    d "Hmmmph..." with dis12
    mc "Oh yeah... that's a good girl..."
    $ renpy.music.set_volume(0.1, delay=5.0, channel='music3')
    play music blowjob2 fadein 5
    show daliablow1 with Dissolve(2.5)
    mc "Ohhhh Jesus..."with dis08
    mc "(She's taking it so fucking deep...)"
    mc "(God, I can feel the tip of my cock slipping down her throat...)"
    mc "(And yet, she keeps taking it in and out without a single gag...)"
    d "*Moans*"
    mc "H-Holy shit, Dalia, you're a fucking natural..."
    mc "It’s so tight... almost feels like a pussy..."
    mc "Ahhh..."
    mc "Your throat’s squeezing me so much..."
    mc "Y-You're enjoying this too, aren't you?"
    d "Mmmmhmm..."
    mc "That’s what I thought... You dirty girl..."
    pause
    mc "Come here, I wanna fuck your juicy mouth..."with dissolve
    d "*Moans*"
    mc "That’s it..."
    play music2 blowjob4 fadein 5
    stop music fadeout 5
    show daliablow2 with dis2
    hide daliablow1
    mc "A-A-Aaaahh f-fuck yes...!" with dissolve
    mc "Oh my god, Dalia...!"
    mc "(It slides in so easily... her throat feels tight, but there’s no resistance...)"
    d "Mmmm...!"
    show daliablow3 with dis17
    hide daliablow2
    mc "Ahhh...." with dissolve
    mc "You're basically drooling, Dalia... You like my cock that much?"
    d "Mmmph..."
    mc "You're doing an amazing job..."
    mc "Oh god..."
    mc "If you wanna stop, just give me a sign, babe..."
    d "Mmm...!"
    mc "(At first I thought she was trying to prove something, but looking at her face I can tell she's enjoying it...)"
    mc "Aaaahhh..."
    mc "Fuck, I don't think anyone could take it so deep and so fast..."
    show daliablow4 with dis17
    hide daliablow3
    mc "Oh f-fuck yeah..." with dissolve
    mc "Do you like getting your mouth fucked, Dalia?"
    d "Hmph... mmph... mmph..."
    mc "That’s it, work all that cum out..."
    mc "(And her tongue gliding on the underside of my dick feels too good, even if it barely has space to move...)"
    pause
    mc "Oh g-god... I think I'm gonna cum..."with dissolve
    mc "I can't hold it...!"
    stop music2
    play sound4 blow1
    play sound6 blow4
    scene cd 60b
    d "*Pulls away and takes several breaths* F-FUCK!" with dissolve
    play sound snow2
    play sound3 sand
    scene cd 61
    d "*Lies back on the sand* J-Jesus...!" with dis08
    d "*Panting* T-Too much... d-dick... N-Need... oxygen!"
    mc "Are you okay?"
    d "*Panting* Fuck yeah, I am..."
    d "It's just that... t-that thing is... too big..."
    d "I couldn't fucking breathe... How do they do that shit in porn!?"
    play sound sand
    show cd 62
    mc "*Getting on top of her* Oh shit, Dalia..."with dis08
    mc "You have no idea how close I am..."
    show cd 63
    d "Oh, that's too bad... poor baby [mc]..."
    show cd 62
    mc "My balls are about to explode..."
    show cd 63
    d "Stop groping me!"
    show cd 62
    mc "Your boobs are fantastic, did I ever tell you that?"
    show cd 63
    d "Never, not even once."
    show cd 65b
    mc "*Pinching her nipples* And your hard nipples give you away – you're horny as fuck..." with dis
    show cd 64
    d "*Giggles* Shut up!"with dis
    show cd 65
    mc "But it's true... isn't it?"
    show cd 64
    d "Perhaps."
    show cd 65
    mc "I want to cum on your pretty face, Dalia..."
    d ". . ."
    show cd 64
    d "{size= 22} Cum in my mouth..."with dissolve
    show cd 65
    mc "I'm sorry, what did you just say?"with dis04
    show cd 64
    d "Cum{w} in{w} my{w} mouth."
    show cd 65
    mc "Would you like that, you pervert? Are you hungry for some cum?"
    show cd 66
    d "Please..." with dis15
    show cd 67
    d "I want you to release your seed in my little mouth..."with dis12
    show cd 66 with dis12
    d "*Whispering* All of it..."with dis
    d "Pretty please..."
    d "Haven't I done such a good job?"
    scene cd 67
    mc "(Oh my god...)"with dis
    mc "Open up for me, babe..."
    play music2 blowjob2 fadein 2
    show daliablow5 with dis17
    blank "{i}Slightly opens her mouth to let your dick in." with dissolve
    mc "Oh, yeah, that's it..."
    d "Mmm..."
    mc "Ahh..."
    mc "(Her lips wrap around me like a second skin...)"
    mc "Oh god, go faster, Dalia..."
    mc "Take it all in..."
    stop music2 fadeout 2
    play music blowjob2 fadein 3
    show daliablow6 with dis15
    hide daliablow5
    mc "AAagh... yeah...!"with dissolve
    d "Mmmph... mmmph... mmph..."
    mc "Oh yeah..."
    mc "You want it so bad, don’t you?"
    d "*Moaning* Mmmmh..."
    mc "You drive me crazy when you look me in the eyes like that..."
    d "Mmmm..."
    mc "F-Fuck, I'm gonna cum so much..."
    mc "Are you sure you can take it?"
    d "Mm-hmmm...."
    stop music fadeout 2
    play music2 blowjob4 fadein 3
    show daliablow7
    hide daliablow6
    mc "*Grabbing her head with both hands and taking control of her movement* AAaahhh... fuck!" with dis15
    mc "Oh... D-Dalia..."
    mc "(Holy shit, I can feel the back of her throat with each thrust...)"
    mc "Oh god, I'm cumming..."
    mc "I'm cumming!!!"
    stop music2
    play sound cum1
    play sound2 cum2
    play sound3 cum3
    scene cd 68
    mc "*Burying your cock balls-deep into Dalia's mouth* AAAAAArgh...!" with hpunch
    play sound4 cum3
    d "Gggh...!"with hpunch
    play sound5 cum3
    d "Ghhhh...."with hpunch
    play sound6 cum3
    mc "*Still cumming* Aaahhh..."with hpunch
    play sound blow4
    show cd 69
    mc "Jesus fucking Christ..." with dis15
    mc "I came like a horse... Are you okay?"
    d ". . ."
    play sound swallow
    show cd 70
    d "*Swallows*" with dis
    d "Mm-hm..."
    mc "Good girl..."

    # CCMOD: ACHIEVEMENT: still waters
    if renpy.loadable("achievements/achievements.rpy"):
        $ award_by_name("Still Waters")

    stop music3 fadeout 7
    play music waves2 fadein 7
    show cd 71 with dis2
    d "*Wipes off her mouth* God..." with dissolve
    d "Strangely, it tastes exactly like I thought it would..."
    show cd 72
    mc "Well, well, well... so you openly admit having fantasized about how my cum tastes, huh...?" with dis12
    show cd 74
    d "Oh, shut up!"with dis15
    show cd 73
    mc "But seriously though, that was... unbelievable!"
    show cd 74
    d "By the amount of... jizz you just dropped in my tummy, I could tell you enjoyed it, yeah."
    show cd 73
    mc "My god, Dalia."
    mc "You can add this to your list of talents."
    show cd 74
    d "*Chuckles* Oh, yeah, it'd look very good on my resume."
    show cd 73
    mc "*Laughs* I'd hire you if that was part of the interview process."
    show cd 74
    d "Anyway, this was... entertaining... but we’ve gotta go now."
    d "I'd leave you here to recover, but this is still my private server! No one can be here without me."
    show cd 73
    mc "No worries, I have no interest in coming to this server if you're not on it..."
    show cd 74
    d "Thank you..."
    d "Well okay, let's go. I wanna go for a run before having dinner."
    show cd 73
    mc "Running? Didn't you just come back from the competition?!"
    show cd 76
    d "*Standing up* I’ve gotta start training NOW if I want to beat Micaela next year!" with dis15
    d "No one's gonna stop me!"
    mc "Hell yeah!"
    mc "(I'm glad she regained confidence in herself.)"
    mc "(God, that ass, though. I need to see that bouncing on top of me one day...)"
    show cd 1
    mc "You know, this was one of the best experiences of my life. We should definitely do this again sometime." with dis2
    d "Never gonna happen again."
    mc "You wanna bet? I could return the favor this time..."
    d "I'm not making any bets with you ever again either."
    mc "Aw..."
    d "And if you talk about what happened here with anyone after we leave this server, I'll murder you."
    d "I swear to god, I'll do it. I'm not kidding."
    mc "I'll k-keep that in mind."
    mc "Can I at least hold onto it in my memories?"
    d "Um... Okay, but make it a hazy memory."
    mc "*Chuckles* Fair enough."
    $ daliablowjob = True
    jump nightmare04

# Used in annie sister map, replaces meeting Annie flashback
# BA/N: modified to trigger more reliably, seems to work?  revert if it breaks anything else
    # has two call spots (mod_call_chat_18 and menurestaurant_mod) for the sake of redundancy
label mod_call_chat_18:
    mct "I know that underpass, it always floods." with dis08
    mct "If I hadn't come from Chang's, I'd be stuck there too."
    show gh 8
    mct "Welp, looks like I’ve got a few minutes to myself until Annie shows up."with dis08
    mct "Maybe I could start asking for the..."
    show gh 9
    mct "Hey... it's Raul and Noah!" 
    mct "I love how I keep running into people I know in this town."
    mct "I don't recognize their friend, though."
    stop music3 fadeout 12
    play music2 mafia fadein 10 volume 0.7
    show gh 10 with Dissolve(3.6)
    giu "Ah, Raul... you’ve got a knack for picking out just the right wine. This one’s got the same rich notes as the vintage back in Palermo." with dis17
    rau "We brought it straight from Bosnia, just for you, old friend." 
    show gh 12
    giu "However... as much as I’m savoring this, I’m here to talk business."with dis17
    show gh 11
    rau "What’s on your mind?"
    rau "Anything specific you need to discuss with me and my brother?"
    show gh 12
    giu "Don’t play the fool with me, Raul. It doesn’t suit you."
    giu "We both know why I'm here."
    giu "I’ve come to deliver one final warning."
    giu "Consider it... a gesture of respect. For all the history between our families."
    show gh 14
    rau "A last warning, he says, brother."
    show gh 15
    rau "Do you have any idea what he’s referring to?"
    rau "No, right?"
    rau "Hmm, you'll have to be more specific."
    show gh 13
    giu ". . ."
    show gh 12
    giu "For over 20 years, the seven big families have maintained a delicate balance."with dis
    giu "El Lobo Mendoza rules over South America, Hugo controls Mexico, Ivanov holds sway in Russia, Hiromi in Asia, Callahan on the East Coast..."
    giu "And finally... you’ve got the West Coast... and I got Europe AND Eternum."
    giu "It’s {i}always{/i} been this way."
    show gh 11
    rau "It started being {i}this way{/i} when Eternum was released and you assumed control of it during an extraordinary meeting where only four of the big families were present."
    show gh 12
    giu "*Sighs* It's simple, really."
    giu "Stay out of Eternum, and we won't have any issues."
    show gh 11
    rau "We never questioned your illegitimate grip on this new market, not for a second."
    rau "But let me remind you, my friend, Eternum is vast. I'm pretty sure it's big enough for the both of us."
    show gh 13
    giu "Hmph."
    show gh 12
    giu "So... is this how it's going to be?"with dis
    giu "You want to start a war? Do you really think you stand a chance with Mendoza and Callahan on my side?"
    show gh 11
    rau "We'd never start a war without provocation."
    rau "That's not how we do business."
    show gh 16
    noa "Please, let's eat first and take a moment to cool down."with dis
    noa "It'd be a shame to let the food go cold."
    show gh 12
    giu "Yeah..."
    giu "You'd be wise to listen to your brother, amico mio."
    giu "Maybe you should have heeded his advice a long time ago..."
    show gh 11
    rau "You might be right about that, old friend."
    rau "You just might be right..."
    play sound risingshort5b
    show gh13 with dis22
    pause 1.5
    show gh11b with dis22
    pause 1.5
    stop music2
    play music3 jazzbar
    stop sound
    scene gh 17
    mct "The fuck is going on over there...?"
    mct "They look tense as hell."
    eul "Hi, handsome."
    show gh 18
    mc "Hmm?" with dis
    mc "Oh, hi there."
    show gh 19
    eul "Can I get you started with a drink while you check out the menu?"
    show gh 18
    mc "Uuh... sure!"
    mc "It almost feels weird being offered alcohol at a restaurant."
    mc "I'm still getting used to this whole “legal adult” thing."
    show gh 19
    eul "Gotta thank former President Stabb for the lowered drinking age."
    show gh 18
    mc "*Chuckles* Yeah, I should probably send him a thank-you card."
    show gh 19
    eul "Can I recommend the Grand Rouge from 2008?"
    show gh 18
    mc "Depends. Will it cost me more than my student loans?"
    show gh 19
    eul "*Giggles* It's actually discounted today. It’s our cheapest wine on the menu, but also one of the best."
    show gh 18
    mc "Well, that's a hard offer to refuse, then."
    show gh 19
    eul "Excellent choice! Would you like to look at the menu too?"
    show gh 18
    mc "I checked it out online, actually. We’re going to have one of those five-course menus, but please don’t start serving until my date arrives."
    show gh 19
    eul "Of course."
    eul "If you need {i}anything{/i} to make your wait shorter, please just let me know."
    show gh 18
    mc "I will, thank you!"
    show gh 20 with dis17
    mct "Damn, service here is top-notch." with dis
    mct "We'll have to leave a good tip, I suppose. I'm still not fully used to how the tipping system works in the US either..."
    play sound vibration
    play sound2 vibration
    bla "{sc=1}Your phone buzzes.{/sc}"
    mct "Oh wow, more messages."
    mct "Feeling popular today."
    menu menurestaurant_mod:
        with dis
        "{color=[walk_points]}[gr]Chang" if changaskmicaelaout and chacha1:
            $ chacha1 = False
            call chat(chang_chat2) from _call_chat_19
            if changborrowjoke:
                $ changmicaela += 1
                mc "*Snorts* (I swear, if Chang doesn't end up with Micaela I'm gonna be even more heartbroken than him.)" with dis08
            else:
                mct "I really want them to end up together, but... bro, there are limits." with dis08
                mct "That joke is way too good."
            jump menurestaurant_mod
        "{color=[walk_points]}[gr]Alex" if alexpath and chacha2:
            $ chacha2 = False
            call chat(alex_chat4) from _call_chat_20
            mct "Damn, Alex has really been pushing herself lately."with dis08
            mct "Since William Bardot basically made her an outcast, she’s been juggling studying, working, and keeping up with her swimming lessons."
            mct "And all on minimum wage."
            mct "If she weren’t so stubborn and let us help her..."
            mct "I’ve got to figure out how to help her without her realizing I’m actually helping her."
            jump menurestaurant_mod
        "{color=[walk_points]}[gr]Nova" if novapath and ((not chacha1 or not changaskmicaelaout) and (not chacha2 or not alexpath)):
            call chat(nova_chat4) from mod_call_chat_21
            if photonovatan:
                mct "Holy smokes, Nova's butt is severely underrated." with dis08
                scene gh 21 
                mct "I have to see those tan lines from the front before they disappear." with dis14
                mct "I wonder how–"
            else:
                mct "Huh, I didn’t even think about that. Entering Eternum without the implant also means all physical impacts carry over to the real world."with dis08
                mct "Interesting."
        "Put your phone away":
            if changaskmicaelaout or alexpath:
                mct "Mmmh, well, I can also reply later." with dis08
                mct "I'll just scroll through Insta and X for a bit."
            else:
                mct "Oh... it was just spam as usual..."
                mct "Well, I guess I'll just scroll through Insta and X for a bit."
            show gh 21
            mct "Heh, I love this new trending meme." with dis14
            mct "It's me for real."
    eul "*Clears throat* Ahem."
    if photonovatan:
        play sound2 whoosh3b
        play soundlow slam3
        play sound plate
        scene gh22
        mc "AAAH!!!{w=0.17}{nw}"
        mc "NO!{w=0.17}{nw}"
        mc "WHA-{w=0.17}{nw}"
        mc "EH-?{w=0.17}{nw}"
        mc "NOT!!{w=0.17}{nw}"
        mc "NOTWHATITSEEMS!"
        scene gh 23
        mc "*Turning around* I wasn't..." with dis12
        mc "I wasn't looking at naked pictures on my phone."
        mc "I was..."
        mc "Please don’t kick me out of the restaurant."
        show gh 34
        eul "*Giggles* Don't worry, sweetheart, I won't tell the manager."
        show gh 23
        mc "I appreciate it."
    else:
        scene gh 23
        mc "*Turning around* Hmm?" with dis12
        mc "Ah, hello again!"
        mc "Is that for me?"
    show gh 34
    eul "I just brought you a little starter. Cream canapes with truffle and cucumber."
    eul "It's on the house, so don't worry about the cost."
    show gh 23
    mc "Ohh... thank you so much!"
    show gh 34
    eul "I just saw you sitting here all alone and figured you'd be hungry."
    show gh 23
    mc "I'm that easy to read, eh?"
    show gh 34
    eul "The kitchen closes in just over an hour, and my shift ends shortly after."
    eul "If you're still feeling... hungry by then, I could help you out. I know some good, cheap spots nearby."
    show gh 23
    mc "Oh..."
    menu:
        with dis
        "{color=[walk_path]}Flirt [red][mt]{s}(Annie Path){/s}":
            $ eulalieflirt = True
            mc "Well... I'll certainly keep it in mind."with dis
            mc "I hate being hungry."
            show gh 34
            eul "*Chuckles* I can imagine..."
            eul "You know, if you're {i}really{/i} hungry, we could even... order room service."
            eul "I've got a room here at the hotel."
            eul "We could drink some wine, play Eternum..."
            show gh 23
            mc "Sounds like a solid plan..."
            eul "Mm-hm..."
        "{color=[walk_points]}[gr]Reject":
            mc "Thank you, but my date must be about to arrive."with dis
            show gh 34
            eul "Yeah, sure..."
            eul "Well... if she ends up not appearing, or if... you just... change your mind... just give me a call."
            eul "Aight?"
            show gh 23
            mc "Uh... sure, thanks for the offer."
    play sound plateputdown
    show gh 35 with dis17
    bla "Eulalie sets the starter on the table and saunters out, deliberately swaying her hips with each step." with dis12
    show gh 70
    if eulalieflirt:
        mct "Wow, this woman's flirting is... direct." with dis15
        mct "I hope Annie doesn't show up when she's saying something awkward."
    else:
        mct "Okay, this woman's definitely hitting on me." with dis15
        mct "I hope Annie doesn’t show up while she’s saying something awkward and get the wrong idea."
    show gh 36
    mct "Hopefully she'll arrive soon, though. I'm starving." with dis
    mc "Hmm."
    mct "At least this little wait helped me shake off those stupid jitters I had earlier."
    mct "You said it yourself. It's just another meal with Annie, like we've normally had these last 10 years."
    mc ". . ."
    mct "Ten years..."
    mct "Man, time flies by."
    mct "Can't believe it's been that long since everything changed."
    mct "10 years and it still feels like it was yesterday."
    mc "Hmph."
    mct "Ten years..."
    stop music3 fadeout 6
    play soundloop town_ambience fadein 7 volume 0.7
    scene gh 37 with Dissolve(3.7)
    show screen tenyearsago
    mct "I remember it clear as day..." with dis15
    mc "*Snorts* Mmh."
    mct "This city sucks ass. This country sucks ass. This continent sucks ass."
    mct "And these stupid buses are crap."
    mc ". . ."
    kid "NO WAAAAY!"
    play music kidsfb fadein 5
    stop soundloop fadeout 22
    show gh 38
    mc "Hmm...?" with dis08
    show gh 39
    kid "WE HAVE THE SAME SHIRT!"
    kid "Where'd you get yours?!"
    show gh 39b
    mc "Uh... online. Probably from the same place you did."
    show gh 39
    kid "No chance, I have no money! My mom got it for me."
    show gh 39b
    mc "Oh... well, I didn't buy mine either. Mom did."
    mc "She got it for my birthday."
    mc "I just told her where to buy it."
    show gh 39
    kid "Uuuhhh... so you know how to use a computer?!"
    show gh 39b
    mc "Erm... I just told her the website, but... yeah, kinda. I guess so."
    show gh 39
    kid "Whoa, cool..."
    c "I'm Chang Wong, by the way!"
    c "I'm 8 years old! Almost 9!"
    show gh 39b
    mc "Oh."
    mc "I'm... [mc]."
    hide screen tenyearsago
    play sound clotheswhoosh
    show gh 40
    c "*Punching the air* Saitama is the best!" with hpunch 
    c "He can beat bad guys with just one punch!"
    mc "...Yeah."
    c "Do you like anime too?"
    show gh 39b
    mc "Uh... yeah, I do."
    show gh 39
    c "Whoa... you're so cool..."
    c "Do you wanna be friends?"
    mc "Um..."
    play sound2 whoosh3b
    play sound3 chair3
    show gh41
    c "*Jumping over the bench* There aren’t a lot of kids around here ‘cause it’s like a business-y area." with hpunch 
    c "And... the kids at school don’t like me much either."
    c "My dad says it’s ‘cause I’m too annoying. And ‘cause I talk too much. But I think it’s ‘cause I’m too mature for my age. Or... at least that’s what my grandma says. She lives in Guangzhou!"
    scene gh 42
    c "By the way, you shouldn't be here alone, you know that?"
    c "You could be kidnapped! Or killed. Or... kidnapped and then killed!"
    show gh 43
    mc "You're alone too!"
    show gh 44
    mc "And I'm not really alone, my dad's inside this office registering our new address."with dis
    mc "We just moved here."
    show gh 45
    c "*Gasps* Wait, so you're gonna live here?!"with dis 
    c "Are you gonna come to our school?!"
    show gh 46
    mc "I guess so."
    show gh 45
    c "*Gasps* That's SO awesome!"
    c "I live here too! My parents have a hotpot restaurant just around the corner! You should totally come someday! Hey, you wanna come too?"
    show gh 46
    mc "Who are you talking to?"
    show gh 45
    c "The girl!"
    show gh 46
    mc "Which girl?"
    show gh 42
    c "The one behind you?"
    show gh 46
    mc "Wha–"
    show gh 47
    mc ". . ." with dis15
    show gh 47b
    mc "Oh..." with dis12
    mc "Hey, Annie."
    mc "Why aren't you with Dad?"
    a ". . ."
    mc ". . ."
    mc "Annie?"
    show gh 49
    c "*Whispering* Do you know each other?"
    show gh 47b
    mc "Yes, she's my-"
    show gh 48
    a "I'm Annie, [mc]'s twin sister."with dis08
    show gh 47b
    c "*Gasps* She can speak!"
    show gh 48
    a "I'm just... shy."
    a "I heard you talking earlier."
    show gh 47b
    a "..."
    mc "This is Chang, Annie."
    show gh 48
    a "Hi Chang."
    a "W-We just moved here..."
    a "Did [mc] already tell you?"
    show gh 47b
    mc "Yep! I did."
    show gh 48
    a "Okay."
    show gh 56
    c "Nice to meet you, Annie!"
    c "Do you want to be my friend, too?"
    show gh 48
    a "S-Sure Chang."
    a "I would like to be your friend."
    show gh 56
    c "Yay! Now we're all friends!"
    show gh 52
    a "B-But I still like [mc] more than you."
    show gh 58
    c "Oh... Ok."
    show gh 52
    a "B-But I like your... s-shirt, Chang."
    show gh 56
    c "OHHH, YOU LIKE ANIME TOO?!"
    show gh 52
    a "Y-Yeah."
    a "I like Sailor Moon."
    show gh 53
    mc "She wanted to be Sailor Moon for Halloween."
    show gh 56
    c "Cool! Do you wanna play with us?! Let's meet at school tomorrow at lunch and pretend to be something we all know!"
    c "How about... Spider-man?!"
    show gh 52
    a "I don't know that one."
    show gh 54
    a "But I like Minions! And Frozen!"with dis08
    show gh 49
    c "Uh... I haven't seen that."
    c "How about... Harry Potter?"
    show gh 48
    a "Haven't seen it yet."
    show gh 49
    c "SpongeBob?"
    show gh 48
    a "No."
    show gh 49
    c "Adventure Time? Pokemon? Transformers?"
    show gh 48
    a "Sorry."
    show gh 49
    c "Eh... Star Wars?"
    show gh 48
    a "I haven't–"
    show gh 54
    a "Wait... yes! We saw it!" with dis06
    a "They were super old movies!"
    show gh 56
    c "Oh, NICE! Let's play that!"
    play sound pop
    play sound2 whoosh6
    show gh 57
    mc "I wanna be Luke!"with pl
    play sound pop
    play sound2 whoosh6
    show gh 54
    a "I wanna be Vader!"with pl
    play sound pop
    play sound2 whoosh6
    show gh 56
    c "I wanna be–" with pr 
    show gh 58
    c "Wait, what? No! I wanna be Vader!"with dis06
    c "You have to be Princess Leia!"
    show gh 59
    a "I don't wanna be Leia, she was so boring."
    a "I wanna be Vader and make everyone go “whoa, she's so strong!”"
    show gh 58
    c "Agh... okay, I'll be Leia."
    show gh 54
    a "Thanks!"
    show gh 60
    c "Alright, so here's the game!"
    c "I have some sticks we can use as lightsabers."
    c "I can put them in my bag and–"
    play sound whoosh6
    play sound2 slam3
    play sound3 leather
    show gh61
    cmom "{sc=2}{size=40}{font=chinafont.ttf}王常！ 你个小兔崽子，说了让你赶紧买完菜回饭店！！！{/sc}"with vpunch 
    cmom "{sc=2}{size=40}{font=chinafont.ttf}你在这坐着干嘛？！{/sc}"with hpunch
    scene gh 62
    c "{sc=2}{size=40}{font=chinafont.ttf}我马上就去！ 我正跟我的朋友说再见呢！！！！{/sc}" with hpunch 
    play sound rubbody
    show gh 63 with dis12
    c "Sorry friends, I gotta go back with my mom now!" with dis12
    c "I'll continue later!"
    show gh 64
    cmom "Yeah, sorry, guys, but Chang’s gotta head out."
    cmom "You can hang out with him all you want after school..."
    show gh 65
    cmom "...as long as he finishes his homework first."
    show gh 63
    c "I'll have them done tomorrow! Promised!"
    c "Don't miss me too much!"
    show gh 54
    a "Guess we still have to wait for Dad..." with dis2
    a "Do you really think we'll see Chang again?"
    show gh 55
    mc "Yeah, he said he's going to our school."
    show gh 54
    a "You really think so...?"
    show gh 55
    mc "Yeah... is something wrong?"
    show gh 48
    a "I don’t want people to disappear again... like with Mom, and Dalia, and Penny..."
    show gh 55
    mc "Awh... don’t worry, you’ll always have me!"
    show gh 66
    a "Then pinky promise!" with dis
    mc "What...? What for?"
    a "Promise you'll never leave me!"
    show gh 67
    mc "Yeah, sure. Pinky promise." with dis
    mc "I'll always be by your side, sis."
    a "Forever!"
    show gh 54
    a "Okay!" with dis12
    a "I'll go see if Dad is done yet!"
    a "Wait here!"
    show gh 55
    mc "I won't go anywhere!"
    show gh 38
    mc ". . ." with dis2
    mct "We made a friend already... and Annie's starting to smile again..."
    mc ". . ."
    play soundlow wood2 volume 0.5
    show gh 68 
    mc "*Swinging your legs* (Maybe it won't suck ass so much after all.)" with dis15
    $ renpy.music.set_volume(0.15, channel='music3')
    stop music fadeout 8
    play music3 jazzbar fadein 6
    scene gh 69 with Dissolve(3.4)
    mc "*Chuckles* Hmm." with dis2
    mct "The day after, we spent the entire afternoon playing together."
    mct "Sometimes, it feels like we're still those kids deep down."
    play sound annierunrest
    stop music3 fadeout 2
    show gh 70
    wai "Hey, hey!" with dis 
    wai "Excuse me, miss, do you have a reservation??" 
    play music2 annielove fadein 4
    show annierestaurant with dis2
    pause 2
    a "{bt=2}*Panting* Aaahh... ahh... aahh... ahh...{w=7.3}{nw}{/bt}" with dis3
    $ unlock_look("annie", 13)
    play soundlow rubbody
    scene gh 71
    a "*Panting* I..." with dis14
    a "*Panting* I-I'm so sorry!"
    a "*Panting* I ran as f-fast as I could, I swear!"
    show gh 72
    mc "But we're definitely not those kids anymore..."
    mc "Wow..."
    show gh 73
    a "What...?"with dis06
    show gh 74
    mc "*Chuckles* Nothing."
    mc "Just thinking."
    show gh 71
    a "I-It's not my fault!" with dis06
    a "That stupid bus took a ridiculous detour, so I decided to walk, b-but I couldn't move fast with these heels, and I was so scared I’d trip and get my hair all messed up, and–"
    show gh 72
    mc "Hey, hey! I haven't even been here that long!"
    mc "No problemo!"
    show gh 71
    a "You sure...?"
    a "But the kitchen closes in just one hour!"
    show gh 72
    mc "Then we'll just have to eat faster!"
    mc "You're here now... and you look absolutely stunning. That's all that matters."
    mc "You've never been more beautiful, Annie."
    show gh 75
    a "Oh... r-really? Do you like the dress?" with dis15
    a "It's... it's new!"
    a "I bought it yesterday."
    a "Along with the shoes, the necklace, and... a new perfume."
    show gh 76
    mc "Everything's perfect."
    mc "All of you."
    show gh 75
    a "Phew... thank goodness."
    a "I was afraid the rain would mess something up."
    a "Or that... I'd be too late and you'd have left already."
    show gh 76
    mc "*Chuckles* As if I could do that. I'd wait all night for you if I had to."
    mc "I’d even ask you to stay standing all night just so I could keep admiring you, but I bet you’re tired."
    mc "Good thing I saved you the best seat in the restaurant!"
    mc "*Pointing at the seat in front of you* M'lady, please..."
    play sound clothes3
    play soundlow ["<silence 1.3>", chair3] volume 0.6
    show gh 77
    bla "Annie sits in front of you with a radiant smile. Her new perfume wafts through the air, captivating your senses." with dis15
    show gh 79
    a "Whew... I was also worried I might be overdressed, but thankfully, there are other women in dresses too."
    show gh 77
    mc "If anything, I’m the one underdressed tonight... sorry about that."
    mc "Next time, I'm gonna show up in a suit, I swear."
    show gh 78
    a "Nah, you look great."
    a "Honestly, you look... perfect."
    show gh 77
    mc "Even the hair?"
    show gh 78
    a "*Giggles* Of course! That messy fringe is just so you."
    show gh 77
    mc "*Chuckles* Thank you for the reassurance."
    mc "And speaking of hair, what did you do to yours?!"
    mc "I knew you were growing it out, but wow!"
    show gh 80
    a "Oh... I didn't do anything too fancy, really." with dis12
    a "I just teased the roots a bit and used a lot of hairspray to... you know, add some volume."
    show gh 81

    # CCMOD: PHONE
    if renpy.loadable("achievements/achievements.rpy"):
        $ unlock_wallpaper_by_name("wp_annie_14")

    mc "You're gonna have to give me the brand of that hairspray."
    show gh 80
    a "Sure thing! It's one Penelope recommended me."
    show gh 81
    mc "*Chuckles* Ah, of course, who else but our personal stylist."
    play soundlow clothes3
    play sound clothes3
    show gh 82
    a "So... tell me, what did you do while you were waiting for me here?" with dis14
    a "*Giggles* Besides, you know, drowning in sadness and yearning, of course."
    show gh 83
    mc "Well, I had some wine, replied to a few messages, and just checked out the place."
    mc "Raul and Noah are here too! But they’re with someone I don’t know, so I figured it’d be best not to interrupt."
    show gh 84
    a "Uhh... you were busy, busy!"
    a "Looks like you don't need me to keep you entertained."
    show gh 85
    mc "Actually, just before you got here, I was reminiscing about the day we arrived in Europe and met Chang."
    show gh 82
    a "Ohh... I'm surprised you still remember that."
    show gh 83
    mc "By all means! When we moved to London, everything felt like it was falling apart. But Chang helped turn that around, and the two of us grew closer than ever."
    mc "I remember every detail of that day."
    show gh 84
    a "Every detail, huh...? Let me check that!"
    a "What was I wearing?"
    show gh 85
    menu:
        with dis
        "Denim overalls over a rainbow-striped t-shirt":
            mc "Denim overalls over a rainbow-striped t-shirt." with dis06
        "A pink hoodie paired with leggings":
            mc "A pink hoodie paired with leggings." with dis06
        "{color=[walk_points]}[gr]An orange shirt tucked into a skirt with suspenders":
            mc "An orange shirt tucked into a skirt with suspenders." with dis06    
            show gh 84
            a "And what were we waiting for?"
            show gh 85
            menu:
                with dis
                "For Chang's hotpot restaurant to open":
                    mc "For Chang's hotpot restaurant to open." with dis06
                "{color=[walk_points]}For Dad to finish the registration [annie_pts]":
                    mc "For Dad to finish the registration." with dis06
                    mc "You bugged him over and over until he was done."
                    $ annie_points += 1
                    play sound beat
                    show screen heartbeat
                    show gh 82
                    a "Wooooooow... impressive memory!"with dis
                    show gh 83
                    mc "Naturally."
                    mc "Unlike you, I’ve got a special place in my mind where I treasure every second I spend with you."
                    show gh 84
                    a "What do you mean, “unlike me”?!"  
                    jump rememberdinnersuccess                
                "For a bus to go see pandas at the zoo":
                    mc "For a bus to go see pandas at the zoo." with dis06
    show gh 84
    a "Wrong!"
    a "SO wrong! *Chuckles* You said that so confidently that you almost made me doubt myself!"
    
    # CCMOD: ACHIEVEMENT: "You Know You Can Rollback?"
    if renpy.loadable("achievements/achievements.rpy"):
        $ award_by_name("You Know You Can Rollback?")
    
    show gh 85
    mc "*Chuckles* In my defense, it was so long ago that no one would remember the details."
    show gh 84
    jump rememberdinnersuccess

# used in base map, add exposition lines towards the end
label poolalex_mod:
    stop music2 fadeout 3
    show b with Dissolve(2.5)
    pause
    show screen afewhourslater with dis12
    pause
    play soundlow schoolbell
    hide screen afewhourslater
    scene ale 38c
    with Dissolve(3)
    pause
    play music2b happy3 fadein 5
    mc "Just 1 more hour, Chang!" with dis
    show ale 38b
    mc "1 more hour and I'll be playing Eternum!" with Dissolve(1.5)
    mc "It's been a long day, but we're almost at the finish line!"
    show ale 39
    c "We should really start studying for next week's exam, though." with dissolve
    c "Especially you... you’re going to be very pre-occupied in the days to come."
    mc "Yeah, it almost seems like Mr. Keating is trying to sabotage me."
    mc "But it doesn't matter much. The subject isn’t that difficult, so I'll just take a look at it the day before and I’m sure I’ll get an A like always. I’ll even settle for a B+."
    c "*Laughs* Goddammit, I’m so jealous of how you always manage to get good grades somehow..."
    c "I wish I was as smart as you..."
    mc "I'm not smart... I just have a good memory, I guess."
    show ale 40
    mc "Also, why the fuck is he also here?! Is he the only teacher in the school?!" with dis
    prof "Um... Yeah, guys, swim class is over. You should probably go take a shower and get back to the fourth floor."
    class "Mr. Keating, do we have to pick this up?"
    prof "I don't know Elijah, I'm just filling in for the swim teacher today. You should ask her when she's back."
    mc "(Ah, always nice to see a man who goes above and beyond for his job.)"
    show ale 41
    c "You know what, I'll go pick that up. If it starts raining it will get ruined."
    mc "Always thinking about others, huh?"
    c "I'm trying to build up some good karma. Always try helping out other people and the universe will be sure to return the favor."
    mc "That's a good philosophy! Alrighty buddy, see you in the locker room."
    c "See you!"
    show ale 42
    d "Well, what did you think of your first swim class here?" with dis
    show ale 42b
    mc "Hey Dalia!"
    mc "(Oh my god, I love this school's swimsuit...)"
    mc "It wasn’t too bad! We actually didn’t have this class at my previous school."
    show ale 42
    d "Are you any good at swimming?"
    show ale 42b
    mc "Good enough. I’m no mermaid, but enough of a decent swimmer to avoid drowning."
    show ale 42
    d "Yeah, kind of like me. I prefer sports that take place on dry land."
    d "Nothing like doing deep squats!"
    d "Ass to grass! Ass to grass!"
    show ale 42b
    mc "*Laughs* True."
    show ale 42
    d "I bet you're super excited to finally play Eternum for the first time."
    show ale 42b
    if dalianaked:
        mc "Well, seeing that you're actually speaking to me again makes me even happier."
        mc "I'm glad you're not still angry with me about what happened yesterday."
        show ale 43
        d "Well, I haven't forgiven you just yet." with dissolve
        d "I still think you're a nasty pervert."
        mc "I'm sorry about that, Dalia."
        mc "I’ll make it up to you somehow, I promise!"
        show ale 42
        d "*Laughs* You better!" with dissolve
        show ale 42b
    else:
        mc "Sure, I am! Can't wait to play it!"
    mc "So... Annie said she'd help me log in for the first time. Will you join us afterward?"
    show ale 44
    d "I can't. I have to hit the gym after school." with dis
    d "I need to follow a strict exercise regimen if I’m to take first place in the upcoming competition."
    show ale 42
    d "But maybe we can play a bit after dinner, if it's not too late." with dis
    show ale 42b
    mc "Sure, sounds good!"
    mc "Real life should always come first."
    mc "So, if I were to guess, I’d say you’re trying to become the school’s top swimmer too?"
    show ale 44
    d "Nah, impossible. Alex is hands down the best swimmer in our school. And the town. And probably even the region." with dis
    mc "Alex?"
    d "Yeah, haven't you seen her? She’s pretty hard to miss."
    mc "Huh?"
    show alex1 with dis
    pause 6.3
    $ alexu = True
    hide alex1
    show ale 44b
    mc "Oh, yeah... I think I’ve seen her before. She’s the one that was swimming fast as fuck, right?" with dis
    d "Hell yeah she was. She could probably even compete in the Olympics if she wanted to."
    mc "She chooses not to?"
    d "Maybe, I don't know. She pretty much keeps to herself."
    d "Sometimes she skips class for a day, sometimes a whole week! Mr. Keating always yells at her for it, but she doesn't seem to care much."
    mc "Oh, so that's why I didn't see her yesterday..."
    show ale 45
    mc "What group is she in?" with dis
    mc "The Jocks? The Populars?"
    show ale 46
    d "She's not in any group. She's a lone wolf." with dis
    mc "Oh, so a bit like you, then?"
    show ale 47
    d "Hmm... maybe." with dis
    d "I don't like being pigeonholed into any \"group\" either."
    d "Maybe that's why we get along."
    mc "Oh, so you two are friends?"
    d "Well, it's hard to get close to her, but yeah, you could say that."
    mc "I see..."
    x "Hey Dalia. Are you gonna hit the showers?"
    show ale 48
    d "Hi Alex! Yeah, I'm coming." with dis
    d "Damn girl, it looked like you were flying on the water today!"
    x "*Laughs* Really? I trained all yesterday. I’m trying to improve my times."
    d "Well, you totally did!"
    play soundlow doorclose2
    show ale 49
    d "*Going down the stairs*" with dis
    mc "Hi!"
    mc "Nice to meet you! I'm [mc]!"
    stop music2b fadeout 6
    play music wind fadein 6
    play soundlow doorclose2
    show ale 50
    x "*Leaves*" with Dissolve(1.2)
    mc "(Um...)"
    mc "(I guess she didn't hear me...)"
    mc "(Anyway, since everyone already left, I should go shower too.)"
    mc "(Only one class to go and then I'll...)"
    play sound punch
    show ale 51 with hpunch
    show ale 51 with hpunch
    pause
    play sound3 fall
    play sound2 fall2
    show ale 52 with dis
    mc "AAArgh... What the fuck..." with dissolve
    show ale 53
    mc "Son of a bitch..." with dis
    show ale 54
    ben "You should be more careful, rookie."
    ben "No running by the pool. You might fall and break your nose."
    show ale 53
    if axelspeak:
        mc "This is your doing, isn’t it, Axel? You filthy rat..."
        if axelpunch:
            mc "Did I hurt you that much yesterday? Had to cry to Papa and tell him all about your ouchie eyeball??"
        mc "Were you so embarrassed that you needed to bring your personal bulldog to intimidate me?"
        mc "2 vs 1? When no one else is around? And you’ve gotta attack me from behind?"
    else:
        mc "You again? What the fuck do you want?"
        mc "Are you so scared of me that you have to attack me from behind?"
    mc "You're both fucking cowards."
    show ale 54
    ben "*Laughs*"
    ben "Nah, it's not like that. It's just that I don't like your stupid, pretty-boy face."
    ben "Or your attitude, strutting around like you’re the king of the world."
    ben "Someone needs to put you in your place."
    show ale 53
    mc "Fuck you. You're a pair of scumbags."
    show ale 54
    ben "You should show some respect when you're talking to Mr. Bardot, you fucking worm."
    ben "You better learn quick, otherwise we’re gonna have to keep teaching you a lesson."
    ben "Be careful, loser."
    mc "Fuck off!"
    show ale 55
    ax "*Laughs*" with Dissolve(1.5)
    ax "I will make your life miserable. I’ll turn your existence into a nightmare."
    ax "For both you and your loved ones."
    mc "Shut the fuck up, dickhead!"
    ax "*Laughs* I almost feel bad for you."
    ax "You messed with the wrong guy."
    ax "Take care, [mc]."
    show ale 56 with Dissolve(1.5)
    play sound doorclose2
    pause
    show ale 57
    mc "*Sighs*" with dis
    mc "(Back in trouble again, [mc]...)"
    mc "(What the fuck is wrong with this guy?)"
    mc "(I've never cared much about bullies, but as soon as he mentioned my \"loved ones\"... I felt a chill down my spine.)"
    mc "(I hope he's just a cocky asshole that’s all talk and nothing else...)"
    show ale 56
    mc "(Anyway, I should get going. I don't want Mr. Keating to give me detention for being late.)" with dis
    mc "(Not today!)"
    stop music fadeout 4
    play soundlow schoolbell
    show ale 58 with Dissolve(3)
    play music2 happy5 fadein 4
    prof "Okay guys, that’s all I’ve got for you." with dissolve
    prof "You’re released to go home."
    play sound2 chairmove
    show ale 59
    mc "(Holy shit, finally!)" with hpunch
    mc "(This was the longest day ever, but it's finally over!)"
    show ale 58
    prof "Oh class, really quick! Before you leave, I need to assign partners for the project that’s due next week."
    prof "The last time I let you pair up on your own, it was utter chaos."
    mc "(What a damn buzzkill...)"
    show ale 60
    prof "Let's see..." with dis
    prof "Um... Chang with Micaela..."
    c "W-What?!"
    show ale 58
    prof "Raul with Noah, Cassie with Aysha, Axel with Benjamin, Dalia with..." with dissolve
    prof "...Charlotte."
    d "Whaaat?" with hpunch
    d "I don't wanna go with her..."
    cha "Excuse me?! I'm the one who should be complaining, bitch!" with hpunch
    show ale 60
    prof "And [mc] with..." with dissolve
    prof "Um..."
    prof "Alex."
    mc "(Uhh...)"
    show ale 61
    x "Huh? Who?" with dis
    prof "[mc]. He and Chang are the two new guys."
    prof "You didn't meet him yesterday because you missed class... again."
    x "[mc]?"
    show ale 62
    x ". . ." with dis
    show ale 63
    x "Ahh... Him..." with dis
    mc ". . ."
    show ale 65 with Dissolve(1.2)
    rau "Mr. Keating, we won't be able to complete this project." with dissolve
    prof "What?! Again?!"
    rau "Yeah, Noah and I have something that we can't postpone."
    prof "This is unacceptable, guys. If this keeps happening, you guys are gonna end up repeating this grade again!"
    rau "Meh, what's one more year?"
    rau "We've grown fond of you, Mr. Keating."
    rau "Anyway, see you next week."
    prof "No! I won't allow it!"
    prof "And what's this \"something\" that can't be postponed?!"
    rau "It's personal."
    prof "I DEMAND TO KNOW!"
    play music2b risinglong fadein 5
    stop music2 fadeout 4
    show raul1 with Dissolve(2.5)
    pause
    show raul2 with dis
    pause
    show raul3 with dis
    pause
    prof "I m-mean..." with dis
    prof "If you don't want to tell me, it's okay..."
    prof "I..."
    hide raul2
    hide raul3
    hide raul1
    show raul1
    rau "Noah's mom is coming to the city." with dis
    hide raul1
    show raul2
    noa "Yeah, I... haven't seen my... mom... for a very long time, Mr. Keating." with dis
    noa "We have to pick her up at the harbor."
    hide raul2
    show raul3
    prof "Oh... T-That's g-great." with dis
    prof "You can do the p-project another day then. N-No problem."
    prof "F-Family comes first."
    hide raul3
    show raul2
    noa "Good." with dis
    hide raul3
    show raul1
    rau "We'd also appreciate if you could keep this information to yourself." with dis
    hide raul1
    show raul2
    noa "My momma is a very shy and reserved woman, Mr. Keating." with dis
    noa "She doesn't like the craziness of daily life."
    noa "And she definitely doesn't like Americans."
    noa "American police, to be more precise. They’re on par with snitches—she believes they should get... stitches."
    hide raul2
    show raul3
    prof "I u-understand!" with dis
    prof "I'll tell everyone you've b-been here all week!"
    hide raul3
    show raul1
    rau "You're a good man, Mr. Keating." with dis
    rau "I'm sure Noah's mom will appreciate it."
    hide raul1
    show raul3
    prof "...G-Give her a k-kiss for me." with dis
    hide raul3
    show raul1
    rau "Oh, we will, Mr. Keating..." with dis
    rau "We will..."
    stop music2b fadeout 4
    play music2 happy5 fadein 3
    show ale 68b
    hide raul1
    with Dissolve(1.2)
    mc "(Hmm? What's up with those two?)" with dissolve
    mc "(Why is Mr. Keating sweating so much?)"
    play sound chairmove
    pause .8
    show ale 69
    mc "Huh?" with dissolve
    show ale 70
    mc "Hey! Alex! Wait!" with dis
    show ale 72 with Dissolve(1.2)
    mc "We have to talk about the project!" with dissolve
    show ale 71
    x "It's Alexandra."
    show ale 72
    mc "What?"
    show ale 71
    x "My name. Alexandra."
    show ale 72
    mc "Oh, yeah, of course. Sorry."
    mc "Um... About the project... We should decide on a day to work on it."
    show ale 71
    x "Yeah, I guess."
    x "This Saturday? Are you free in the afternoon?"
    show ale 72
    mc "Sure, sounds good."
    mc "I'd say we could do it at my place, but there’s a lot of people there and we’d probably need to work somewhere more quiet..."
    show ale 71
    x "We can go to my house. I'm normally by myself on Saturdays."
    mc "(Nice...)"
    show ale 72
    mc "Sweet!"
    mc "Do you know what we could do the project on?"
    mc "Mr. Keating said we had to write a paper on something related to the topic of social control."
    mc "Maybe we could write about the influence of the media? Or about a cult! Have you heard about the Sons of..."
    show ale 71
    x "We can talk about it on Saturday."
    show ale 72
    mc "Oh... yeah, of course."
    mc "Um..."
    mc "By the way, I'm [mc]. I saw you before, at the pool."
    show ale 71
    x "Yes, I know."
    show ale 72
    mc "Oh... I thought you didn't notice me."
    show ale 71
    x "Anything else?"
    show ale 72
    mc "Um..."
    menu:
        with dis
        "Compliment her tattoos":
            $ alexpen = False
            mc "Can I tell you something?" with dis
            mc "I love your tattoos."
            mc "I noticed them at the pool and..."
            show ale 73
            x "Yeah, yeah, okay." with dis
            x "I’ve heard it all before. You don’t need to kiss my ass, alright?"
            x "I don't need any new friends."
            mc "Oh... I just..."
            x "What are you gonna mention next?"
            x "My hair? Yeah, it's ashen. Swimming? Yep, I'm pretty good at it. Thanks, but no thanks."
            show ale 75
            mc "Um..." with dis
            mc "(Damn, she's a tough one to talk to...)"
            show ale 74
            x "Are we done?"
            show ale 75
            mc "I... guess so, yeah."
        "Compliment her swimming skills":
            $ alexpen = False
            mc "Can I tell you something?" with dis
            mc "You're the best swimmer I've ever seen."
            mc "I saw you at the pool and..."
            show ale 73
            x "Yeah, yeah, okay." with dis
            x "I’ve heard it all before. You don’t need to kiss my ass, alright?"
            x "I don't need any new friends."
            mc "Oh... I just..."
            x "What are you gonna mention next?"
            x "My hair? Yeah, it's ashen. My tattoos? Yep, I have a lot of them. Thanks, but no thanks."
            show ale 75
            mc "Um..." with dis
            mc "(Damn, she's a tough one to talk to...)"
            show ale 74
            x "Are we done?"
            show ale 75
            mc "I... guess so, yeah."
        "Compliment her hair":
            $ alexpen = False
            mc "Can I tell you something?" with dis
            mc "I love your hair."
            mc "I noticed how cool it looked when you got out of the pool and–"
            show ale 73
            x "Yeah, yeah, okay." with dis
            x "I’ve heard it all before. You don’t need to kiss my ass, alright?"
            x "I don't need any new friends."
            mc "Oh... I just..."
            x "What are you gonna mention next?"
            x "My tattoos? Yeah, I have a lot of them. Swimming? Yep, I'm pretty good at it. Thanks, but no thanks."
            show ale 75
            mc "Um..." with dis
            mc "(Damn, she's a tough one to talk to...)"
            show ale 74
            x "Are we done?"
            show ale 75
            mc "I... guess so, yeah."
        "{color=[walk_points]}Compliment her pen [pink][mt](Alex +1)":
            mc "Can I tell you something?"with dis
            mc "You have a nice pen."
            show ale 73
            x "Um... Excuse me? My... pen?"with dis
            show ale 75
            mc "Yeah, I happened to notice it earlier and it's a good one. Good brand. Made of good quality materials."with dis
            x ". . ."
            show ale 74
            x "Are you seriously complimenting me on that?"
            x "My fucking pen?"
            show ale 75
            mc "Erm... Yes?"
            show ale 74
            x "Aren't you gonna mention my hair? My tattoos? That you saw my swimming at the pool?"
            show ale 75
            mc "Uhh... Should I?"
            mc "I mean, your hair is... pretty hairy...? And yeah, I saw you swimming, but it wasn’t anything to write home about..."
            mc "To be honest, I could probably swim faster than you if I trained seriously."
            mc "And now that you mention it... yeah, looks like it's true, you have some tattoos."
            mc "Cool, I guess."
            x ". . ."
            mc ". . ."
            x ". . ."
            $ alex_points += 1
            play sound "beat.ogg"
            show ale 76
            show heartr at topleft
            with dissolve
            hide heartr with dissolve
            pause
            show ale 78
            x "Maybe you're not just another boring dummy after all." with dis
            x "I like your style."

            # CCMOD: PHONE
            if renpy.loadable("achievements/achievements.rpy"):
                $ unlock_wallpaper_by_name("wp_alex_1")

            show ale 77
            mc "Oh well... thanks."
            mc "Was it something I said?"
            show ale 78
            x "No, it's what you didn't say. I don't like having my ass kissed, or having everyone tell me over and over what they think I want to hear."
            x "I like your sarcasm... [mc]."
            x "You said you were Dalia's friend?"
            show ale 77
            mc "Yeah, we’ve known each other since we were little."
            # ===== new stuff =====
            if im_incest_mode=="incest":
                show ale 74
                x "Now that I think about, Dalia did mention having younger siblings before." with dis
                x "How are you in the same class as us?"
                show ale 75
                mc "*Chuckles* I was actually born later that same year, close enough for us to be in the same grade."
                mc "The other younger sibling is my twin sister, so she's also in our grade."
                mc "She's in a different class though."
                show ale 78
                x "Oh, wow. That's quite the family." with dis
                x "Well, you and Dalia probably the only people in this class that are actually worth talking to. Maybe your twin would be, too."
            else:
                show ale 74
                x "Now that I think about, Dalia did mention having a brother before." with dis
                x "You're younger aren't you? How are you in the same class as us?"
                show ale 75
                mc "*Chuckles* I was actually born later that same year, close enough for us to be in the same grade."
                show ale 78
                x "So you're practically twins, huh?" with dis
                x "Well, you two are probably the only people in this class that are actually worth talking to."
            # ===== end changes =====
            show ale 77
            mc "Thanks, but I don't like having my ass kissed."
            show ale 78
            x "*Chuckles* Well... anything else, [mc]?"
            show ale 77
            mc "Hmm... nope, I think that was all."
    show ale 79
    x "Cool. I'll see you tomorrow. Peace." with dis
    mc "Sure. Goodbye, Alex!"
    show ale 80
    x "Alexandra." with Dissolve(.8)
    mc "Oh... shit, yeah sorry, I forgot."
    mc "Didn't Dalia call you Alex, though?"
    x "She can do it. You can't."
    mc "Gotcha."
    mc "Goodbye, Alexandra."
    x "Bye."
    play sound doorsliding
    show ale 81 with Dissolve(1.5)
    mc "(Hmm...)" with dissolve
    mc "(She seems... interesting.)"
    mc "(Let's see how Saturday's meeting goes.)"
    mc "*Looking at your phone* Hmm..."
    mc "(Oh shit!)" with hpunch
    mc "(I have to go home!!)" with hpunch
    mc "(IT’S ETERNUM TIME!)" with hpunch
    jump preeternum

# Used in annie sister map, wholesale replacement due to interfering lines
label preeternum_mod:
    stop music2 fadeout 5
    play sound2 keys
    play music2b tictoc fadein 4
    scene welcome 6 with Dissolve(3.5)
    play sound doorclose
    mc "Go, go, go!" with dissolve
    play sound3 stairsrun
    show login 15 with Dissolve(2.3)
    play sound4 doorclose
    mc "Annie?" with dissolve
    play sound5 dooropen1
    show login 16 with dis
    a "Finally!" with dissolve
    a "Let's go, bro! We're already late!"
    mc "*Laughs* Already got your Eternum E-Suit on, I see!"
    a "Of course! Now, come on already!"
    mc "Okay, okay!"
    play sound dooropen1
    show login 17 with Dissolve(1.6)
    mc "Let's get star- Oh crap, I don't have an E-Suit yet!" with dissolve
    show login 18
    a "It should've been included with the game." with dis
    a "Did you look through everything in the box?"
    show login 17
    mc "Ohhh... that makes sense." with dis
    mc "To be honest... no, I didn't. I only took out the implant to charge it."
    mc "So... do I need to put on the whole suit?"
    show login 18
    a "Yep!" with dis
    a "I mean, technically you only really need the visor and neural implant connected, but without the suit, you might experience some bugs during your gameplay."
    a "You don’t want a buggy playthrough, do you?"
    show login 17
    mc "Hell no!" with dis
    mc "But... does that mean that you're playing right now? Are you inside Eternum?"
    show login 18
    a "Of course not! I'd be sitting still if I was, remember?" with dis
    show login 17
    mc "Oh. You always played in your room, so I never wanted to come in and bother you." with dis
    show login 19
    a "Well, I'm not playing yet, so I can remove my visor at any time." with dis
    show login 20
    a "See?" with dis
    mc "Nice!"
    show login 21
    a "Alright then, let's not waste any more time!"with dis
    a "Put on the E-Suit. I won’t look."
    mc "No need to look way, sis. I don't mind."
    a "H-hey now! We're not little kids anymore!"with hpunch
    mc "*Laughs* Okay, okay..."
    play sound clothes
    a "First I'll help you connect your neural implant and visor, and then after you're all set up, I'll go to my room to log in myself."
    a "You’re gonna start off by talking to the Eternum Lady. It’s a required step for all new players."
    a "I should be connected by the time you're done, and then all you’ll have to do is accept the invitation to my server."
    mc "Got it."
    mc "I'm ready."
    show login 22
    a "Nice! That suit looks good on you!" with dis
    a "Now sit down!"
    play sound chair1
    show login 23 with dis
    mc "And now what?" with dissolve
    a "You just have to insert the E-3X implant under your skin and then connect the other end to the visor."
    mc "T-The what?? Under my what?!"
    show login 24
    a "Don't worry, it’ll sting only a tiny bit! I bet you won't even feel it." with dis
    mc "Okay, if you sa-"
    play sound plugin
    mc "FUCK!!" with hpunch
    a "Sorry! Did that hurt?!"
    mc "N-No, no, I barely felt it..."
    a "Alright, now put on the visor..."
    play sound2 plugin
    a "This goes there..."
    play sound3 plugin
    a "And then this here..."
    a "And now..."
    play soundlow login
    show evisor
    pause 3
    mc "Wow!" with dis
    a "Is it working?"
    mc "Yeah! I mean, I don't know, all I see is blue."
    hide evisor
    show login 25
    a "Then it's working! Awesome! You're officially connected to Eternum!" with dis
    a "This will only happen on your very first time, don't worry. After that, the loading will be much faster."
    a "You should be getting access any moment now..."
    a "First, you'll lose the sense of feeling in your legs."
    a "After that, your sense of hearing will seem to fade away."
    a "Lastly, your vision will slowly start to blur and then you won’t be able to see this room anymore."
    stop music2b fadeout 3
    mc "Hmmm... now that you mention it, it does kind of feel like my legs have fallen asleep or something..."
    show login 26 with dis
    pause
    mc "Hmm? Three what?" with dissolve
    mc ". . ."
    show login 27
    mc "Oh damn, I can't hear you!" with dis
    mc "I can't hear a thing!"
    mc "Two what? Is it something important?"
    show login 28
    mc "Hey, sis?!" with dis
    mc "C-Can we stop for a second?"
    mc "Oh shit, I forgot to go to the bathroom..."
    mc "I hope I don’t lose control of my bowels next..."
    show login 29
    mc "Annie!"with dis
    mc "Why are you making that face?"
    mc "Is something wrong?!"
    jump eternum