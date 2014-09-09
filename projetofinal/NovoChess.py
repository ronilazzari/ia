"""
GUI for use with ChessBoard by John Eriksson. Designed to be imported in chess programs, but allows
stand-alone use. It supports drag and drop piece movement, board flipping, arbitrary board/square size
and arbitrary placement in a Pygame window larger than the board.

Known issues: - Promotion dialog not yet implemented --> it automatically promotes to queen now

License: GPL
Jasper Stolte <JasperStolte@gmail.com>
"""

__version__ = '0.2'
__program__ = 'ChessBoardGUI'
__author__ = 'Jasper Stolte <JasperStolte@gmail.com>'
__copyright__ = 'Copyright (C) 2006 Jasper Stolte'

## version 0.2: Adapted for PGU
## version 0.1: First playable version

## Todo: - Implement dialog for promotion
##       - Make nicer messagebox
##       - Add other piece image sets

from ChessBoard import ChessBoard
import pygame, os
from pygame.locals import *


DONE_ANIMATING = pygame.USEREVENT + 40
DRAG_COMPLETE = pygame.USEREVENT + 41

class Board_view:
    """Contains a board image, and the piece images."""

    pygame.font.init()
    font = pygame.font.Font(None, 36)
    pics_loaded = False
    piece_files = {'p':'b_pawn', 'r':'b_rook','b':'b_bishop', 'n':'b_knight', 'q':'b_queen', 'k':'b_king', 'P':'w_pawn', 'R':'w_rook','B':'w_bishop', 'N':'w_knight', 'Q':'w_queen', 'K':'w_king'}
    promote = {'q':ChessBoard.ChessBoard.QUEEN, 'r':ChessBoard.ChessBoard.ROOK, 'b':ChessBoard.ChessBoard.BISHOP, 'n':ChessBoard.ChessBoard.KNIGHT}

    def __init__(self, squaresize, flipped = False):
        """Display empty board."""
        
        self.game = ChessBoard.ChessBoard()                              # The game associated with the view
        self.position = self.game.getBoard()                             # The current position as defined in ChessBoard
        self.board = self.make_board(squaresize)                         # The empty board (can also be a nice image)
        self.static_image = pygame.Surface((8*squaresize,8*squaresize))  # This will contain everything except the moving piece
        self.squaresize = squaresize                                     # Size of the squares
        self.pieces = {}                                                 # Dictionary of images of chesspieces
        
        self.dirtyrects = []
        self.moving_piece = None
        self.animated_pieces = []
        self.flipped = flipped


    def paint(self, surface):
        if not self.pics_loaded:
            for piecetype, piece_file in self.piece_files.iteritems():
##                file_name = os.path.join("data\piecesets\classic", self.piece_files[piecetype]+'.png')
                file_name = os.path.join("Data/piecesets/igor", self.piece_files[piecetype]+'.png')
##                file_name = os.path.join("data\piecesets\gorman", self.piece_files[piecetype]+'.png')
                image = pygame.image.load(file_name).convert_alpha()
                #image.set_colorkey(image.get_at((0,0)))
                image = pygame.transform.scale(image, (self.squaresize,self.squaresize))
                self.pieces[piecetype] = image        
            self.pics_loaded = True
            self.setup()
        surface.blit(self.static_image, [0,0])
        self.update(surface)
        self.dirtylist = []
        pygame.display.update(Rect(surface.get_abs_offset(),(8*self.squaresize,8*self.squaresize)))

    def reset(self):
        self.game.resetBoard()
        self.position = self.game.getBoard()
        self.moving_piece = None
        self.animated_pieces = []
        self.setup()


    def setup(self):
        """Places the pieces on the board"""

        if not self.pics_loaded: return
        self.position = self.game.getBoard()
        self.static_image.blit(self.board, [0,0])
        for col in range(8):
            for row in range(8):
                piecetype = self.position[row][col]
                if piecetype != '.':
                    posx, posy = self.screenpos_from_board((col,row))
                    self.static_image.blit(self.pieces[piecetype], [self.squaresize*posx, self.squaresize*posy])
         
        
    def make_board(self, squaresize):
        """Construct board images out of light and dark squares."""
        
        board = pygame.Surface([8*squaresize,8*squaresize])
        light = pygame.Surface([squaresize, squaresize])
        light.fill([255,206,158])
        dark = pygame.Surface([squaresize, squaresize])
        dark.fill([209,139,71])

        for x in range(4):
            for y in range(4):
                board.blit(light, [2*x*squaresize, 2*y*squaresize])
                board.blit(dark, [(2*x+1)*squaresize, 2*y*squaresize])
                board.blit(light, [(2*x+1)*squaresize, (2*y+1)*squaresize])
                board.blit(dark, [2*x*squaresize, (2*y+1)*squaresize])

        return board

    def flip(self):
        """Flip the board coordinates."""
        
        if self.flipped: self.flipped = False
        else: self.flipped = True
        self.setup()

    def click(self, clickpos):
        """Selects a piece for draggin upon mouseclick."""

        if self.moving_piece != None: return False
        
        (x,y) = clickpos
        x = x / self.squaresize
        x = max(x,0)
        x = min(x,7)
        y = y / self.squaresize
        y = max(y,0)
        y = min(y,7)
        boardx, boardy = self.boardpos_from_screen((x,y))

        piecetype = self.position[boardy][boardx]
        if piecetype != '.':
            piecerect = pygame.Rect(self.squaresize*x, self.squaresize*y, self.squaresize, self.squaresize)
            clickedfield = self.board.subsurface(piecerect)
            self.static_image.blit(clickedfield, piecerect)
            self.dirtyrects.append(piecerect)

            origin = (x,y)
            self.moving_piece = MovingPiece(piecetype, origin)            
            self.moving_piece.lastrect = piecerect
        return True

    def release(self, releasepos):
        """Releases the selected piece, and generates a move for the engine."""

        if not self.moving_piece: return None
        
        from_pos = self.moving_piece.origin
        self.moving_piece = None
        
        (x,y) = releasepos
        if x < 0: x = 0
        if x > 7*self.squaresize: x = 7*self.squaresize
        if y < 0: y = 0
        if y > 7*self.squaresize: y = 7*self.squaresize            

        to_pos = self.boardpos_from_screen((x/self.squaresize, y/self.squaresize))
        return (from_pos, to_pos)


    def check_move(self, move):
        """Check whether a move is valid, and execute it on screen."""

        (from_pos, to_pos) = move
        result = self.game.addMove(from_pos, to_pos)
        if not result and self.game.getReason() == self.game.MUST_SET_PROMOTION: return self.game.MUST_SET_PROMOTION

        if result:
            self.position = self.game.getBoard()
            self.do_move(self.screenpos_from_board(from_pos), self.screenpos_from_board(to_pos))
            self.game.setPromotion(0)
            return 0
        else:
            self.no_move(from_pos)
            return self.game.getReason()
                    

    def update(self, surface):
        """Plots a new frame, used when moving a piece"""

        rectlist = []
        for rect in self.dirtyrects:        # Clean stuff up first
            updated = self.static_image.subsurface(rect)
            surface.blit(updated, rect)
            rectlist.append(rect)
        self.dirtyrects = []        

        done_animating = []
        for p in self.animated_pieces:      # Plot the automatic moving pieces
            p.time_taken += p.timer.tick()
            if p.time_taken >= p.total_time:
                p.time_taken = p.total_time         # To prevent overshoot on the last pic
                self.do_move(p.origin, p.destination, keep_animating=True) # Finish the animation
                done_animating.append(p)            # Remove it from the list
            orix,oriy = p.origin
            destx, desty = p.destination
            interx = int((destx - orix)*self.squaresize*p.time_taken/p.total_time)
            intery = int((desty - oriy)*self.squaresize*p.time_taken/p.total_time)
            inter_rect = pygame.Rect(interx+orix*self.squaresize, intery+oriy*self.squaresize, self.squaresize, self.squaresize)
            surface.blit(self.pieces[p.piecetype], inter_rect)
            rectlist.append(inter_rect)
            self.dirtyrects.append(inter_rect)
        for p in done_animating:        # Removing while in the iteration causes glitches, so I took it out of the loop.
            self.animated_pieces.remove(p)
            if self.moving_piece and self.moving_piece.origin == p.destination: self.moving_piece = None
            if not len(self.animated_pieces):
                pygame.event.post(pygame.event.Event(DONE_ANIMATING, {}))

        if not self.moving_piece: return rectlist
    
        offsetx, offsety = surface.get_abs_offset() # Now plot the piece that is clicked
        newx,newy = pygame.mouse.get_pos()
        newx -= self.squaresize/2
        newx -= offsetx
        if newx < 0: newx = 0        
        if newx > 7*self.squaresize: newx = 7*self.squaresize
        
        newy -= self.squaresize/2
        newy -= offsety
        if newy < 0: newy = 0
        if newy > 7*self.squaresize: newy = 7*self.squaresize        
        newrect = pygame.Rect(newx,newy, self.squaresize, self.squaresize)
        
        surface.blit(self.pieces[self.moving_piece.piecetype], newrect)
        self.lastrect = newrect
        rectlist.append(newrect)
        self.dirtyrects.append(newrect)

        return rectlist
        

    def no_move(self, from_pos):
        """Move was invalid, visually restore the board to old position"""
        
        posx, posy = from_pos
        rect = pygame.Rect(posx*self.squaresize, posy*self.squaresize, self.squaresize, self.squaresize)
        piecetype = self.position[posy][posx]
        self.static_image.blit(self.pieces[piecetype], rect)
        self.dirtyrects.append(rect)


    def do_move(self, source, dest, animated=False, keep_animating=False):  # Uses screen coordinates
        """Visually moves pieces according to the input move."""

        if not keep_animating:
            remove = []                 # Finish old moves if necessary
            for p in self.animated_pieces:
                remove.append(p)                    
            for p in remove:
                self.animated_pieces.remove(p)
                self.do_move(p.origin, p.destination, keep_animating=True)

        orix, oriy = source             # Clear the source square
        orirect = pygame.Rect(orix*self.squaresize, oriy*self.squaresize, self.squaresize, self.squaresize)
        underground = self.board.subsurface(orirect)
        self.static_image.blit(underground, orirect)
        self.dirtyrects.append(orirect)

        boardx, boardy = self.boardpos_from_screen(dest)    
        destx, desty = dest             
        sourcex, sourcey = self.boardpos_from_screen(source)
        piecetype = self.position[boardy][boardx]

        special = self.game.getLastMoveType()
        if special == self.game.KING_CASTLE_MOVE:
            if piecetype.lower() == 'k':
                if self.flipped: self.do_move((0,source[1]),(2,source[1]), animated, keep_animating=True)
                else: self.do_move((7,source[1]),(5,source[1]), animated, keep_animating=True)
        elif special == self.game.QUEEN_CASTLE_MOVE:
            if piecetype.lower() == 'k':
                if self.flipped: self.do_move((7,source[1]),(4,source[1]), animated, keep_animating=True)
                else: self.do_move((0,source[1]),(3,source[1]), animated, keep_animating=True)
        elif special == self.game.EP_CAPTURE_MOVE:
            targetx, targety = self.screenpos_from_board((boardx, sourcey))
            targetrect = pygame.Rect(targetx*self.squaresize, targety*self.squaresize, self.squaresize, self.squaresize)
            underground = self.board.subsurface(targetrect)
            self.static_image.blit(underground, targetrect)
            self.dirtyrects.append(targetrect)

        if animated:
            piece = AnimatedPiece(piecetype, source, dest, 600)
            self.animated_pieces.append(piece)
            return

        destrect = pygame.Rect(destx*self.squaresize, desty*self.squaresize, self.squaresize, self.squaresize)
        piece = self.pieces[piecetype]          # Place the piece on its new location
        underground = self.board.subsurface(destrect)
        self.static_image.blit(underground, destrect)
        self.static_image.blit(piece, destrect)
        self.dirtyrects.append(destrect)

                      
                
    def ask_promote(self):           ## Should be a dialog or something. For now, autoqueen.
        """Selects which piece to promote a pawn to."""
        
        if self.game.getTurn(): return 'q'
        else: return 'Q'
        

    def boardpos_from_screen(self, screenpos):
        """Converts a screen coordinate to a board coordinate."""

        screenx, screeny = screenpos
        if not self.flipped: return (screenx, screeny)
        else: return (7-screenx, 7-screeny)
        

    def screenpos_from_board(self, boardpos):
        """Converts a board coordinate to a screen coordinate."""

        boardx, boardy = boardpos
        if not self.flipped: return (boardx, boardy)
        else: return (7-boardx, 7-boardy)

    def screenpos_from_notation(self, notation):    # Example: 'e2'
        files = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
        ranks = {"8":0,"7":1,"6":2,"5":3,"4":4,"3":5,"2":6,"1":7}
        x = files[notation[0]]
        y = ranks[notation[1]]
        return self.screenpos_from_board((x,y))
        

    def message(self, message, surface):
        """Displays a message on the screen."""

        text = self.font.render(message, 1, (160,120,200)).convert()
        text.fill((0,0,0))
        textpos = text.get_rect(centerx = surface.get_width()/2, centery = surface.get_height()/2)
        surface.blit(text, textpos)
        text = self.font.render(message, 1, (160,120,200))
        surface.blit(text, textpos)
        pygame.display.update(Rect(surface.get_rect().move(surface.get_abs_offset())))


class AnimatedPiece:
    def __init__(self, piecetype, origin, destination, total_time):
        self.piecetype = piecetype
        self.origin = origin        # In screen coordinates
        self.destination = destination
        self.total_time = total_time

        self.lastrect = None
        self.time_taken = 0
        self.timer = pygame.time.Clock()
        self.timer.tick()

class MovingPiece:
    def __init__(self, piecetype, origin):
        self.piecetype = piecetype
        self.origin = origin        # In screen coordinates
        self.lastrect = None
        

if __name__ == "__main__":
    (offset_x, offset_y) = BOARD_OFFSET = (0,0)
    SQUARESIZE = 65

    screen = pygame.display.set_mode((8*SQUARESIZE, 8*SQUARESIZE))
    pygame.display.set_caption("A drag and drop GUI for ChessBoard, version 0.1")

    board_surface = screen.subsurface((offset_x, offset_y, 8*SQUARESIZE, 8*SQUARESIZE))
    view = Board_view(SQUARESIZE)
    view.paint(board_surface)
    
    done = False
    gameover = False
    pygame.event.set_allowed([USEREVENT + 1, QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
    pygame.time.set_timer(pygame.USEREVENT + 1, 20)
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            if gameover: continue
            if event.type == MOUSEBUTTONDOWN:
                view.click((event.pos[0]-offset_x, event.pos[1]-offset_y))
            elif event.type == MOUSEBUTTONUP:
                if view.moving_piece == None: continue
                move = view.release((event.pos[0]-offset_x, event.pos[1]-offset_y))                
                result = view.check_move(move)
                if result == view.game.MUST_SET_PROMOTION:
                    view.game.setPromotion(view.game.QUEEN)
                    view.check_move(move)
                if view.game._game_result:
                    view.update(board_surface)
                    result = view.game.getGameResult()
                    if result == view.game.WHITE_WIN: view.message("Checkmate! White wins.", board_surface)
                    elif result == view.game.BLACK_WIN: view.message("Checkmate! Black wins.", board_surface)
                    elif result == view.game.STALEMATE: view.message("Stalemate! Draw.", board_surface)
                    elif result == view.game.FIFTHY_MOVES_RULE: view.message("Draw due to the 50 moves rule.", board_surface)
                    elif result == view.game.THREE_REPETITION_RULE: view.message("Draw due to repetion.", board_surface)
                    gameover = True
                if False and not gameover and view.game.getTurn() ^ view.flipped:
                    view.flip()     # Flipping on every move turned off, because it becomes annoying after a while.
                    view.paint(board_surface)
            elif event.type == USEREVENT + 1:
                rectlist = view.update(board_surface)
                if not rectlist: continue
                screenrectlist = []
                for r in rectlist:
                    screenrectlist.append(r.move(offset_x, offset_y))
                pygame.display.update(rectlist)
                
        pygame.time.wait(5)
        
    pygame.display.quit()
