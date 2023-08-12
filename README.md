# 🌟 Coffee Shop RPG ☕ 🌟
Welcome to our humble coffee shop where we serve the finest coffee and cafe drinks in the world. For our coffee beans we use only the best offerd by coffee farmers around the world. Ladies and Gentlemen please enjoy your day with our special made coffee to your hearts desire. It needs to be said that we work for customer satisfaction and our staff are trained to serve you the best taste with the best manners. Now, The journey begins 🪶>>>

### Maktab 98 🚀

## 🔥 Programming Team 🔥
### Group 2 >>>
### Scrum Master: Alireza Arvin
### Team Leader: Mahdi yar kafaie khou
### Developer: Zahra Mahjour
### Developer: Sevda Hayati
### Developer: Mohammad Ali Soltan Hosseini

## Project Details 💻 👏	
This is a Django Fullstack Project and it features a website to order coffee in a coffee shop in tehran city(The Quest city). It uses django version 4.2.3 (The God of Frameworks) to bring all the new features into the code(The Pain and Suffering of Programmers). We used all the knowledge we gained so far (XP Gained) to code a website for the wise manager(The Demon Lord) who tasked us with this group project(Literally the Quest). the project tasks start with a general knowledge over the project structure(Buying Wepons and Healing Potions). As we learned from the details, first we needed to draw an ERD(World Map) then build the base of the project using django frame-work from there we had to choose our site interface template to style the site(Choose the way to procede with your quest). once all of these steps were done we could finaly start the main coding of the app. We bring to you our best, using all we learned from Maktab 98.

## Project Sprints
With all said and done we now start the story of our progress in the project >>>

### Sprint 1 Start with Basics & Build Design

#### ERD(Entity Relationship Diagram)
Everything starts with a good planning, in our case: we programmers need to draw the ERD for our project so we could configure the base build of our database which alows us to build upon it. you can see our team effort below. first step, so chill...

<img width="100%" src="ERD(v11).png">


#### Template 
Choosing a good template was a group effort as well, there were so many obstacles but we could overcome them and choose a good template.

<img width="100%" src="Screen1.jpg">


But as you just realized we need to customize this template since it is actually a food bar site. the reason why we chose this is It's simplicity and dominant beauty. Chill, this is going to work. (^-^)


#### Project Setup
In this step the setup for the project is configured and we begin to get into code. The starting apps are staff & coffeeshop. yay, hooray.


#### Git Init
The git repo was initiated and the files of the project were pushed on the github.

#### Basic Models 
The first build of models in the project are done. using django models module, the basic models that got accepted by our teachers were: 
- Staff(User)
- Order
- OrderItem
- CafeItem
- Review
- ParentCategory
- SubCategory

#### Basic Templates
The Basic layout of the site templates was created in this step(django tags & starting templates).

#### Authentication
A very tricky and chalenging step in the first sprint of the project but it was done with Style and Elegance. The custome authentication had to be done using phone number. At first it was thought that we need a complete backend for User in this project but then we realized that it wasn't the case, We only needed to customize the username to phone-number. It is a cruel world...

#### OTP(One Time Password)
In the process of the project a problem was surfaced, which was the security of the user accounts and trust issues of the project. So it was decided to implant an otp system to solve this problem. This system sends a 6-digit one time password to the user which then, the user can use to authenticate into website. Going round and round and round...

#### First Theme Setup
It was time to finally bring the site up with some styles in it. So we thought to do these templates using the chosen theme for the website:
- base.html
- navbar.html
- header.html
- footer.html

#### Gathering Data for the Website
We just realized that we have no idea about what we are going to put on our cafe website.< we are programmers not coffee makers >. So the solution was the answer we always get from our teachers: Go search for it yourself (0_0).

#### Views & Templates (FBVs)
At first we thought we had to use generic class based view's, Yet as you can guess we were told to use function based views. just imagine the feeling we had...
So we said ok, chill, lets go with the flow and with a broken heart we did the functions...
As you can guess the pages were brought up one after the other. Starting with pages, first came the home page, then the menu page, and then the high difficulty ones came... they were called checkout page and cart page. At this point it's hard to belive that we could survive all that :|

FBVs for Pages:
- home.html
- menu.html
- checkout.html
- cart.html

#### Cookies & Sessions
A realy hard task in the journey, not many could survive this. But your dear bros were just defeted as expected. now we beg for points from the manager(demon lord)... please have mercy on us!
cookies were done but it was done blindly without having any view functions written so we had to change them alot.
it works so dont touch it!


And with this last step of the first sprint came to an end.
Our journy for the coffee continues...