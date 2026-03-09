from puzzle import Puzzle
import pygame
import pygame_gui
import time
import colors

SCREEN_SIZE = (1280, 720)

#Setup
pygame.init()
BASICFONT = pygame.font.Font('FiraCode-Retina.ttf',50)

pygame.display.set_caption('8 Puzzle')
window_surface = pygame.display.set_mode(SCREEN_SIZE)
background = pygame.Surface(SCREEN_SIZE)
background.fill(pygame.Color(colors.BABY_PINK))
manager = pygame_gui.UIManager(SCREEN_SIZE, 'theme.json')

# Rights: https://iconmonstr.com/puzzle-19-png/
programIcon = pygame.image.load('logo.png')
pygame.display.set_icon(programIcon)

pygame_gui.core.IWindowInterface.set_display_title(self=window_surface,new_title="8-Puzzle")

def display_elements():
    #Elements
    ### Title Label
    pygame_gui.elements.ui_label.UILabel(manager=manager,
                                        text="8-Puzzle Game",
                                        relative_rect=pygame.Rect((540, 10), (300, 70)),
                                        object_id="#title_box"
                                        )
    


display_elements()
### solve button
solve_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1000, 640), (250, 45)),
                                             text='Solve Puzzle',
                                             manager=manager,
                                             object_id="#solve_btn")
print("Solve button created successfully!")

### algorithmOptions DropDown
dropdown_layout_rect = pygame.Rect((970, 600), (280, 35))
algorithmOptions = ["A* (Manhatan Distance)","Best-First (Manhatan Distance)"]
algorithmDropDown = pygame_gui.elements.UIDropDownMenu(options_list=algorithmOptions,
                                                       starting_option=algorithmOptions[1],
                                                       relative_rect=dropdown_layout_rect,
                                                       manager=manager)

### puzzle size dropdown
size_dropdown_rect = pygame.Rect((970, 550), (280, 35))
sizeOptions = ["3x3", "4x4", "5x5"]
sizeDropDown = pygame_gui.elements.UIDropDownMenu(options_list=sizeOptions,
                                                  starting_option=sizeOptions[0],
                                                  relative_rect=size_dropdown_rect,
                                                  manager=manager)
print("Size dropdown created successfully!")
print(f"Size dropdown options: {sizeOptions}")
print(f"Size dropdown starting option: {sizeOptions[0]}")

### Search label
pygame_gui.elements.ui_label.UILabel(parent_element=algorithmDropDown,
                                     manager=manager,
                                     text="Heuristic Search:", # (pos-width,pos-height),(width,height)
                                     relative_rect=pygame.Rect((800, 600), (170, 30)))

### Size label
pygame_gui.elements.ui_label.UILabel(parent_element=sizeDropDown,
                                     manager=manager,
                                     text="Puzzle Size:", # (pos-width,pos-height),(width,height)
                                     relative_rect=pygame.Rect((800, 550), (170, 30)))

### Final state input
report_rect = pygame.Rect((1000, 210), (250, 30))
Final_state = pygame_gui.elements.UITextEntryLine(relative_rect=report_rect,
                                                  manager=manager)

### Final state label
pygame_gui.elements.ui_label.UILabel(parent_element=Final_state,
                                     manager=manager,
                                     text="Final State:", # (pos-width,pos-height),(width,height)
                                     relative_rect=pygame.Rect((855, 210), (140, 30)))

### set final state with button
set_final_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1000, 250), (250, 30)),
                                                text='Set Final State',
                                                manager=manager)
### shuffle button
button_layout_rect = pygame.Rect((1000, 290), (250, 30))
shuffle_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                             text='Shuffle',
                                             manager=manager)

### change size button
change_size_rect = pygame.Rect((1000, 500), (250, 30))
change_size_button = pygame_gui.elements.UIButton(relative_rect=change_size_rect,
                                                 text='Apply Size Change',
                                                 manager=manager)
print("Change size button created successfully!")

### info button
info_html = "<b>Click Here<b>To see developers info!!!"
button_layout_rect = pygame.Rect((1250, 690), (30, 30))
info_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                             text='?',
                                             manager=manager,
                                             tool_tip_text=info_html)
### alert label
alert_label = pygame_gui.elements.ui_label.UILabel(
                                     manager=manager,
                                     text="",
                                     relative_rect=pygame.Rect((920, 320), (250, 30)),
                                     object_id="#accept_label")


def draw_blocks(blocks):
    for block in blocks:
        if block['block'] != 0:
            pygame.draw.rect(window_surface, colors.PINK_GROTTO, block['rect'])
            # Adjust font size based on block size
            block_size = min(block['rect'].width, block['rect'].height)
            font_size = max(20, int(block_size * 0.6))
            font = pygame.font.Font('FiraCode-Retina.ttf', font_size)
            textSurf = font.render(str(block['block']), True, colors.NAVY_PINK)
            textRect = textSurf.get_rect()
            textRect.center = block['rect'].center
            window_surface.blit(textSurf, textRect)
        else:
            pygame.draw.rect(window_surface, colors.ROYAL_PINK, block['rect'])

def solveAnimation(moves):
    print(f"Starting animation with {len(moves)} moves")
    try:
        for i, mv in enumerate(moves):
            print(f"Move {i+1}/{len(moves)}: {mv}")
            zero = puzzle.matrix.searchBlock(0)
            if mv == "right":
                puzzle.matrix.moveright(zero)
            elif mv == "left":
                puzzle.matrix.moveleft(zero)  
            elif mv == "up":
                puzzle.matrix.moveup(zero)
            elif mv == "down":
                puzzle.matrix.movedown(zero)
            else:
                print(f"Unknown move: {mv}")
                continue
                
            puzzle.setBlocksMatrix()
            draw_blocks(puzzle.blocks)
            pygame.display.update()
            time.sleep(0.2)
        print("Animation completed successfully!")
    except Exception as e:
        print(f"Error in solveAnimation: {e}")
        import traceback
        traceback.print_exc()
        
def createNewPuzzle(grid_size):
    """Create a new puzzle with the specified grid size"""
    global puzzle
    # Adjust puzzle size based on grid size
    base_size = 330
    if grid_size == 4:
        puzzle_size = 400
    elif grid_size == 5:
        puzzle_size = 450
    else:
        puzzle_size = base_size
    
    puzzle = Puzzle.new(250, 220, puzzle_size, puzzle_size, grid_size)
    puzzle.initialize()
    return puzzle

window_surface.blit(background, (0, 0))
pygame.display.update()
clock = pygame.time.Clock()
puzzle = Puzzle.new(250, 220, 330, 330)
puzzle.initialize()
algorithm = "Best-First (Manhatan Distance)"
current_size = 3
fstate="1,2,3,4,5,6,7,8,0"
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == shuffle_button:
                    puzzle.randomBlocks()
                elif event.ui_element == change_size_button:
                    # Apply the size change
                    print("Change size button clicked!")
                    alert_label.set_text("Button clicked! Processing...")
                    
                    try:
                        # Get the current selection from dropdown
                        selected_text = sizeDropDown.selected_option
                        print(f"Selected text: {selected_text}")
                        
                        new_size = int(selected_text.split('x')[0])
                        print(f"New size: {new_size}, Current size: {current_size}")
                        
                        if new_size != current_size:
                            print("Creating new puzzle...")
                            current_size = new_size
                            puzzle = createNewPuzzle(current_size)
                            print("Puzzle created, generating final state...")
                            fstate = puzzle.generateDefaultFinalState()
                            Final_state.set_text(fstate)
                            alert_label.set_text(f"Changed to {selected_text} puzzle!")
                            print("Size change completed successfully!")
                        else:
                            alert_label.set_text(f"Already using {selected_text} puzzle!")
                    except Exception as e:
                        alert_label.set_text(f"Error: {str(e)}")
                        print(f"Error in change size button: {e}")
                        import traceback
                        traceback.print_exc()
                elif event.ui_element == set_final_button:
                    if not puzzle.setBlocks(Final_state.get_text()):
                        alert_label.set_text("Final state invalid!")
                    else:
                        alert_label.set_text("Final state valid!")
                        puzzle.final_state = Final_state.get_text()
                elif event.ui_element == info_button:
                    Info_msg = '<b>8-Puzzle Solver<br><br>Authors:</b><br>Mateus Mendonça Monteiro<br>Vinicius Santana Ramos'
                    # Information Box - Info
                    info_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                            manager = manager,
                                                                                            action_long_desc = Info_msg,
                                                                                            window_title ='Developers Info',
                                                                                            )
                elif event.ui_element == solve_button:
                    print("Solve button clicked!")
                    alert_label.set_text("Solving puzzle...")
                    
                    try:
                        print(f"Selected algorithm: {algorithm}")
                        print(f"Current puzzle size: {puzzle.grid_size}")
                        print(f"Puzzle matrix: {puzzle.matrix.getMatrix()}")
                        print(f"Final state: {puzzle.final_state}")
                        
                        # Test basic functionality first
                        print("Testing basic puzzle functionality...")
                        test_matrix = puzzle.matrix.getMatrix()
                        print(f"Test matrix shape: {test_matrix.shape}")
                        
                        # Check if puzzle is already solved
                        print("Checking if puzzle is already solved...")
                        from matrix import Matrix
                        final_state_matrix = Matrix(puzzle.grid_size, puzzle.grid_size)
                        final_state_matrix.buildMatrix(puzzle.final_state)
                        print(f"Final state matrix: {final_state_matrix.getMatrix()}")
                        
                        if puzzle.matrix.isEqual(final_state_matrix.getMatrix()):
                            alert_label.set_text("Puzzle is already solved!")
                            print("Puzzle is already solved!")
                        else:
                            print("Puzzle needs solving, checking solvability...")
                            if not puzzle.isSolvable():
                                alert_label.set_text("Puzzle is not solvable!")
                                print("Puzzle is not solvable!")
                            else:
                                print("Puzzle is solvable, starting algorithm...")
                                if algorithm == "Best-First (Manhatan Distance)":
                                    print("Running Best-First algorithm...")
                                    moves = puzzle.bestFirst()
                                    print(f"Best-First completed. Moves found: {len(moves)}")
                                    if moves:
                                        tempo = "{temp: .5f} seconds".format(temp = puzzle.lastSolveTime)
                                        report_msg = '<b>Visited nodes:</b> '+str(puzzle.cost)+'        <b>Time:</b>'+tempo+ '        <b>Resolution:</b> '+str(len(moves))+' steps'
                                        # Confirmation Box - Algorithm Report
                                        confirmation_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                                manager = manager,
                                                                                                                action_long_desc = report_msg,
                                                                                                                window_title =algorithm.split(" ")[0] + ' Search Report',
                                                                                                                )
                                        print("Starting solve animation...")
                                        solveAnimation(moves)
                                        print("Solve animation completed!")
                                    else:
                                        alert_label.set_text("No solution found!")
                                        print("No solution found!")
                                    
                                elif algorithm == "A* (Manhatan Distance)":
                                    print("Running A* algorithm...")
                                    moves = puzzle.a_star()
                                    print(f"A* completed. Moves found: {len(moves)}")
                                    if moves:
                                        tempo = "{temp: .5f} seconds".format(temp = puzzle.lastSolveTime)
                                        report_msg = '<b>Visited nodes:</b> '+str(puzzle.cost)+'        <b>Time:</b>'+tempo+ '        <b>Resolution:</b> '+str(len(moves))+' steps'
                                        # Confirmation Box - Algorithm Report
                                        confirmation_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = pygame.Rect((600, 300), (180, 80)),
                                                                                                                manager = manager,
                                                                                                                action_long_desc = report_msg,
                                                                                                                window_title =algorithm.split(" ")[0] + ' Search Report',
                                                                                                                )
                                        print("Starting solve animation...")
                                        solveAnimation(moves)
                                        print("Solve animation completed!")
                                    else:
                                        alert_label.set_text("No solution found!")
                                        print("No solution found!")
                                else:
                                    print(f"Unknown algorithm: {algorithm}")
                                    alert_label.set_text(f"Unknown algorithm: {algorithm}")
                            
                    except Exception as e:
                        alert_label.set_text(f"Solve error: {str(e)}")
                        print(f"Error in solve button: {e}")
                        import traceback
                        traceback.print_exc()
                        
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == algorithmDropDown:
                    algorithm = event.text
                elif event.ui_element == sizeDropDown:
                    # Automatically apply size change when dropdown changes
                    try:
                        selected_text = event.text
                        new_size = int(selected_text.split('x')[0])
                        if new_size != current_size:
                            current_size = new_size
                            puzzle = createNewPuzzle(current_size)
                            fstate = puzzle.generateDefaultFinalState()
                            Final_state.set_text(fstate)
                            alert_label.set_text(f"Changed to {selected_text} puzzle!")
                    except Exception as e:
                        alert_label.set_text(f"Error: {str(e)}")
                        print(f"Error in size dropdown: {e}")
            elif event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_element == Final_state:
                print("")
        manager.process_events(event)
        
        
    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    draw_blocks(puzzle.blocks)
    pygame.display.update()
