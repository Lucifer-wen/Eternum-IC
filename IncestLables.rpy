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

# Used in annie sister map
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
    mc "*Laughs* And Penelope the preteen that was too \"cool\" to play with her younger siblings?"
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
    d "Oh, y-yeah, so excited! Hi bro!"
    p "It's been a while!"
    d "Yeah, welcome back!"
    mc "Thanks!"
    mc "So good to see you, sis!"
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
    n "Both of those things can wait! You didn't even welcome your brother and sister properly!"
    n "They're gonna live with us for a whole year. You know that, right?"
    show welcome 12
    p "But we just did!"
    show welcome 13b
    p "[mc]! I can't wait to properly meet you!" with dis
    p "I wish I could stay, but I really need to go!"
    show welcome 13a
    p "Oh, and you must be Annie! Nice to see you again!"
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
    # $ _im_choice_let_them_go = im_walk_menu("Let them go", good=True)
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
        "Let them go [pink][mt](Penelope, Dalia +1)":
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
            d "Because he's cool! It's good to see the city didn't change you, bro." with dis
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
    d "Kredon's annual race is next week!"
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
    a "Goodnight bro! Sweet dreams!" with dis
    show welcome 26
    n "Tomorrow is your first day at your new school, so it's probably a good idea to get a good night’s rest."
    n "Goodnight, [mc]."
    mc "See you tomorrow!"
    jump dream1

# Used in base map
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
    if nancy03scene:
            mc "(Those abs... is it bad that I want to lick them? Well, after what happened with Mom...)"
    else:
            mc "(Those abs... is it bad that I want to lick them?)"
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
    d "{size=15}Fuck it"
    mc "What did you say?"
    show cd 34
    d "I said okay... let's do it."
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
    if nancy03scene:
            mc "(Oh... fuck yeah! Screw it! No matter if she's my sister, I already did it with my mom, so this can't be any worse.)"
    else:
            mc "(Oh... fuck yeah! My sister’s gonna give me a blowjob!)"
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
label mod_call_chat_21:
    if photonovatan:
        mct "Holy smokes, Nova's butt is severely underrated." with dis08
        scene gh 21 
        mct "I have to see those tan lines from the front before they disappear." with dis14
        mct "I wonder how–"
    else:
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
    # $ _im_choice_flirt = im_walk_menu("Flirt", good=False)
    # $ _im_choice_reject = im_walk_menu("Reject", good=True)
    menu:
        with dis
        "[red]Flirt":
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
        "[gr]Reject":
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
    mct "You said it yourself. It's just another meal alone with Annie, like we’ve usually had these last 10 years."
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
    mc "You wanted to be Sailor Moon once."
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
    a "Wait... yes! I saw it!" with dis06
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
    # $ _im_choice_pandas = im_walk_menu("For Dad to finish the registration", good=True)
    menu:
        with dis
        "Denim overalls over a rainbow-striped t-shirt":
            mc "Denim overalls over a rainbow-striped t-shirt." with dis06
        "A pink hoodie paired with leggings":
            mc "A pink hoodie paired with leggings." with dis06
        "An orange shirt tucked into a skirt with suspenders":
            mc "An orange shirt tucked into a skirt with suspenders." with dis06    
            show gh 84
            a "And what were we waiting for?"
            show gh 85
            menu:
                with dis
                "To go to Chang's house":
                    mc "To go to Chang's house." with dis06
                "[gr]For Dad to finish the registration":
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
                "A bus to go see pandas at the zoo":
                    mc "A bus to go see pandas at the zoo." with dis06
    show gh 84
    a "Wrong!"
    a "SO wrong! *Chuckles* You said that so confidently that you almost made me doubt myself!"
    show gh 85
    mc "*Chuckles* In my defense, it was so long ago that no one would remember the details."
    jump rememberdinnersuccess
