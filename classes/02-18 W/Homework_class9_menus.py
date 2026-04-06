'''
We want to create a command line driven menu system with 4 levels

1. Clients
    1. Select Client
        1. View Client Summary
        2. Manage Client Cash
    2. Create Client
        1. New Individual
        2. New Joint

2. Portfolios
    1. Trade
        1. Buy
        2. Sell
    2. Performance
        1. Holdings Snapshot
        2. P/L Report

1st level                                   (Clients LHS,                             |                  Portfolios RHS)
2nd level              (Select Client,                         Create Client)         |        (Trade,                  Performance)
3rd level (View Client Summary, Manage Client Cash)    (New Individual, New Joint)    |      (Buy, Sell)         (Holdings Snapshot, P/L Report)
4th leaf  (View Client Summary, Manage Client Cash)    (New Individual, New Joint)    |      (Buy, Sell)         (Holdings Snapshot, P/L Report)


The left hand side (LHS) is provided below. Your job:

1) complete the right hand side (RHS)
    a) Hint: this is copy and paste
    b) changing what gets printed

2) explain in your own words what the program does
    a) Try to include state, transitions and invariants
    b) Does menu control come from logic or program structure

The program is a 4-level comand line menu system. 

State: The main state variable is "break_to_top", which is a boolean that tracks whether
the user has hit a leaf endpoint and needs to be sent back to the top level menu. It starts as False at the beginning of 
every top-level loop iteration and gets set to True when the user reaches a leaf. Each nested while loop checks this flag at 
the top before doing anything, so once it's True the loops unwind one at a time until we're back at level 1.
 
Transitions: The user moves deeper into the menu by making a numbered choice. They move back up by entering nothing (None), which 
triggers a break one level up. When they hit a leaf, break_to_top gets set to True, which causes each enclosing loop to break in 
sequence until control returns to the outermost while loop where break_to_top gets reset to False.
 
Invariant: break_to_top is only ever reset to False at the top level. As long as it stays True, every nested loop will 
immediately break without redisplaying its menu. This guarantees no duplicate menus get shown during the unwind.
 
Does menu control come from logic or program structure?... Mostly program structure. The nesting of while loops mirrors 
the menu hierarchy directly, so the depth of the loop is the depth of the menu. The logic (if/elif chains and the break_to_top flag) 
handles transitions between states, but the structure of the code itself is what defines the menu tree.
 

3) assume you are at a leaf endpoint. Instead of returning to level 3
   return to level 1

4) How many discrete paths are in this menu system

8 discrete paths.

'''
'''
OIM 3600 - Menu Navigation Assignment Rubric
--------------------------------------------

Student Name: ______________________
Score: ______ / 100


FUNCTIONAL REQUIREMENTS (70 pts)
--------------------------------

TOP / CLIENTS / PORTFOLIOS NAVIGATION (30 pts)

[ ] TOP menu displays correctly
[ ] Can navigate TOP → CLIENTS → back to TOP
[ ] Can navigate TOP → PORTFOLIOS → back to TOP
[ ] No infinite loops
[ ] No accidental fall-through (one choice triggers one action)


PORTFOLIO BRANCH IMPLEMENTATION (20 pts)

[ ] Portfolio branch fully implemented
[ ] At least one working leaf under PORTFOLIOS
[ ] Back behavior correct within portfolio branch


EXIT-TO-TOP BEHAVIOR (20 pts - A-level feature)

[ ] “Return to Top” works from at least one CLIENT leaf
[ ] “Return to Top” works from at least one PORTFOLIO leaf
[ ] No duplicate menus printed after return
[ ] No stuck loops after return
[ ] to_top cleared only at TOP level


CONTROL FLOW QUALITY (15 pts)

[ ] Correct one-level unwind via break
[ ] Each loop checks to_top appropriately
[ ] No unnecessary nested flag logic
[ ] Code readable and logically structured


STI EXPLANATION (15 pts)

[ ] Identifies key state variables (to_top, etc.)
[ ] Correctly defines transitions
[ ] States invariant about unwinding
[ ] Distinguishes state vs control flow


GRADE BANDS
-----------

C (70-79)
- Honest attempt
- Portfolio branch partially implemented
- Some unwind logic present
- STI explanation minimal or partially incorrect

B (80-89)
- Both branches work correctly
- One-level back behavior correct
- No infinite loops
- STI explanation identifies state, transitions, invariant

A (90-100)
- Exit-to-top works from leaf level (both branches)
- No duplicate menus or stuck loops
- to_top handled cleanly
- STI explanation clearly distinguishes state vs control flow
'''


'''
THIS ASSIGNMENT WILL BE DUE 2/25 (NEXT WEDNESDAY) SO YOU CAN ASK QUESTIONS NEXT MONDAY (2/23)
'''



import functions2 as fn2

while True:
    break_to_top = False
    fn2.clear_screen()
    fn2.print_header('Top Menu level 1')
    options=['Clients', 'Portfolios'] #level 1 options
    fn2.display_menu(options)
    choice = fn2.get_menu_choice(options)

    if choice is None:
        print('exit top level menu')
        fn2.pause(1)
        break
    elif choice == 1:
        while True:
            if break_to_top: break
            fn2.clear_screen()  
            fn2.print_header('Clients level 2')
            options=['Select Client', 'Create Client'] #level 2 options
            fn2.display_menu(options)
            choice = fn2.get_menu_choice(options)

            if choice is None:
                print('return to level 1')
                fn2.pause(1)
                break
            elif choice == 1:
                while True:
                    if break_to_top: break
                    fn2.clear_screen()
                    fn2.print_header('Select Client level 3')
                    options=['View Client Summary', 'Manage Client Cash'] #level 3 options
                    fn2.display_menu(options)
                    choice = fn2.get_menu_choice(options)

                    if choice is None:
                        print('return to level 2')
                        fn2.pause(1)
                        break
                    elif choice == 1:
                        # no while statement leaf
                        fn2.clear_screen()
                        fn2.print_header('View Client Summary level 4')
                        # no options leaf
                        print('you have reached View Client Summary')
                        print('returning to level 3') 
                        fn2.pause(1)
                        break_to_top = True
                        continue # not needed but shows intent
                           
                    elif choice == 2:
                        # no while statement leaf
                        fn2.clear_screen()
                        fn2.print_header('Manage Client Cash level 4')
                        # no options leaf
                        print('you have reached Manage Client Cash')
                        print('returning to level 3') 
                        fn2.pause(1)
                        break_to_top = True
                        continue # not needed but shows intent

            elif choice == 2:
                while True:
                    if break_to_top: break
                    fn2.clear_screen()
                    fn2.print_header('Create Client level 3')
                    options=['New Individual', 'New Joint'] #level 3 options
                    fn2.display_menu(options)
                    choice = fn2.get_menu_choice(options)

                    if choice is None:
                        print('return to level 2')
                        fn2.pause(1)
                        break
                    elif choice == 1:
                        # no while statement leaf
                        fn2.clear_screen()
                        fn2.print_header('New Individual level 4')
                        # no options leaf
                        print('you have reached New Individual')
                        print('returning to level 3') 
                        fn2.pause(1)
                        break_to_top = True
                        continue # not needed but shows intent
                           
                    elif choice == 2:
                        # no while statement leaf
                        fn2.clear_screen()
                        fn2.print_header('New Joint level 4')
                        # no options leaf
                        print('you have reached New Joint')
                        print('returning to level 3') 
                        fn2.pause(1) 
                        break_to_top = True
                        continue # not needed but shows intent   
    elif choice == 2:
        while True:
            if break_to_top: break
            fn2.clear_screen()
            fn2.print_header('Portfolios level 2')
            options=['Trade', 'Performance'] #level 2 options
            fn2.display_menu(options)
            choice = fn2.get_menu_choice(options)

            if choice is None:
                print('return to level 1')
                fn2.pause(1)
                break
            elif choice == 1:
                while True:
                    if break_to_top: break
                    fn2.clear_screen()
                    fn2.print_header('Trade level 3')
                    options=['Buy', 'Sell'] #level 3 options
                    fn2.display_menu(options)
                    choice = fn2.get_menu_choice(options)

                    if choice is None:
                        print('return to level 2')
                        fn2.pause(1)
                        break
                    elif choice == 1:
                        fn2.clear_screen()
                        fn2.print_header('Buy level 4')
                        print('you have reached Buy page')
                        print('returning to top level')
                        break_to_top = True
                        fn2.pause(1)
                        continue

                    elif choice == 2:
                        fn2.clear_screen()
                        fn2.print_header('Sell level 4')
                        print('you have reached Sell page')
                        print('returning to top level')
                        break_to_top = True
                        fn2.pause(1)
                        continue

            elif choice == 2:
                while True:
                    if break_to_top: break
                    fn2.clear_screen()
                    fn2.print_header('Performance level 3')
                    options=['Holdings Snapshot', 'P/L Report'] #level 3 options
                    fn2.display_menu(options)
                    choice = fn2.get_menu_choice(options)

                    if choice is None:
                        print('return to level 2')
                        fn2.pause(1)
                        break
                    elif choice == 1:
                        fn2.clear_screen()
                        fn2.print_header('Holdings Snapshot level 4')
                        print('you have reached Holdings Snapshot')
                        print('returning to top level')
                        break_to_top = True
                        fn2.pause(1)
                        continue

                    elif choice == 2:
                        fn2.clear_screen()
                        fn2.print_header('P/L Report level 4')
                        print('you have reached P/L Report')
                        print('returning to top level')
                        break_to_top = True
                        fn2.pause(1)
                        continue












    