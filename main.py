import pygame
import random

pygame.init()


class MovingCard(object):
    moved = False
    moved_card = []
    card_d = ()
    cards = None
    score = 0
    font = pygame.font.SysFont('bahnschrift', 36)

    def clicking_up(self, deck_list):
        if len(self.moved_card) > 0:
            for item in deck_list:
                if not isinstance(item, DeckTwo):
                    if item.check_position() and item.checking_card(self.moved_card):
                        item.adding_card(self.moved_card)
                        self.score += 5
                        self.moved = False
                        self.moved_card = []
                        if isinstance(self.cards, DeckOne):
                            self.cards.showing_card()
                        self.cards = None
                        break
            else:
                self.cards.adding_card(self.moved_card)
                self.moved = False
                self.moved_card = []
                self.cards = None

    def draw(self, screen, card_dict):
        if self.moved:
            pos = pygame.mouse.get_pos()
            x = pos[0] - self.card_d[0]
            y = pos[1] - self.card_d[1]
            for item in self.moved_card:
                screen.blit(card_dict[item], [x, y])
                y += 32

    def display_score(self, screen):
        score_value = self.font.render("Очки: " + str(self.score), True, (255, 255, 255))
        screen.blit(score_value, (20, 675))

    @staticmethod
    def file_handling(score):
        with open('score.txt', 'a') as file:
            file.write("Очки: %s \n" % score)


class Deck(object):
    def __init__(self, x, y):
        self.cards = []
        self.rect = pygame.Rect(x, y, 71, 96)

    def check_position(self):
        pos = pygame.mouse.get_pos()
        if self.rect.left <= pos[0] <= self.rect.right:
            if self.rect.top <= pos[1] <= self.rect.bottom:
                return True
            else:
                return False
        else:
            return False


class DeckOne(Deck):
    def __init__(self, x, y):
        Deck.__init__(self, x, y)
        self.y = y
        self.hidden = []

    def extend_list(self, lst):
        self.hidden.extend(lst)
        self.cards.append(self.hidden.pop())
        if len(self.hidden) > 0:
            for i in range(len(self.hidden)):
                self.rect.top += 32

    def draw_the_card(self, screen, card_dict):
        surface_alpha = screen.convert_alpha()
        surface_alpha.fill([0, 0, 0, 0])
        pygame.draw.rect(surface_alpha, (255, 255, 255, 64), [self.rect.left, self.rect.top, 71, 96], 2)
        screen.blit(surface_alpha, (0, 0))
        i = self.y
        if len(self.hidden) > 0:
            for _ in self.hidden:
                screen.blit(card_dict["back_side"], [self.rect.left, i])
                i += 32
        if len(self.cards) > 0:
            for item in self.cards:
                screen.blit(card_dict[item], [self.rect.left, i])
                i += 32

    def adding_card(self, card):
        if len(self.cards) > 0 or len(self.hidden) > 0:
            for i in range(len(card)):
                self.rect.top += 32
        else:
            for i in range(len(card)):
                if i > 0:
                    self.rect.top += 32
        self.cards.extend(card)

    def clicking_down(self, card):
        if len(self.cards) > 0:
            top = self.rect.top
            lst = []
            for i in range(len(self.cards)):
                if self.check_position():
                    pos = pygame.mouse.get_pos()
                    lst.insert(0, self.cards.pop())
                    card.card_d = (pos[0] - self.rect.left, pos[1] -
                                   self.rect.top)
                    card.moved = True

                    card.cards = self
                    card.moved_card.extend(lst)
                    if len(self.cards) > 0 or len(self.hidden) > 0:
                        self.rect.top -= 32
                    break
                else:
                    lst.insert(0, self.cards.pop())
                    self.rect.top -= 32
            else:
                self.rect.top = top
                self.cards.extend(lst)

    def showing_card(self):
        if len(self.cards) == 0 and len(self.hidden) > 0:
            self.cards.append(self.hidden.pop())

    def checking_card(self, moved_card):
        card = moved_card[0]
        result = False
        if len(self.cards) == 0:
            if "king" in card:
                result = True
        else:
            if "hearts" in card or "diamonds" in card:
                if "spades" in self.cards[-1] or "clubs" in self.cards[-1]:
                    next_card = "X"
                    if "king" in self.cards[-1]:
                        next_card = "queen"

                    elif "queen" in self.cards[-1]:
                        next_card = "jack"
                    elif "jack" in self.cards[-1]:
                        next_card = "10_"
                    elif "10_" in self.cards[-1]:
                        next_card = "9_"
                    elif "9_" in self.cards[-1]:
                        next_card = "8_"
                    elif "8_" in self.cards[-1]:
                        next_card = "7_"
                    elif "7_" in self.cards[-1]:
                        next_card = "6_"
                    elif "6_" in self.cards[-1]:
                        next_card = "5_"
                    elif "5_" in self.cards[-1]:
                        next_card = "4_"
                    elif "4_" in self.cards[-1]:
                        next_card = "3_"
                    elif "3_" in self.cards[-1]:
                        next_card = "2_"
                    elif "2_" in self.cards[-1]:
                        next_card = "ace"

                    if next_card in card:
                        result = True
            elif "hearts" in self.cards[-1] or "diamonds" in self.cards[-1]:
                next_card = "X"
                if "king" in self.cards[-1]:
                    next_card = "queen"
                elif "queen" in self.cards[-1]:
                    next_card = "jack"
                elif "jack" in self.cards[-1]:
                    next_card = "10_"
                elif "10_" in self.cards[-1]:
                    next_card = "9_"
                elif "9_" in self.cards[-1]:
                    next_card = "8_"
                elif "8_" in self.cards[-1]:
                    next_card = "7_"
                elif "7_" in self.cards[-1]:
                    next_card = "6_"
                elif "6_" in self.cards[-1]:
                    next_card = "5_"
                elif "5_" in self.cards[-1]:
                    next_card = "4_"
                elif "4_" in self.cards[-1]:
                    next_card = "3_"
                elif "3_" in self.cards[-1]:
                    next_card = "2_"
                elif "2_" in self.cards[-1]:
                    next_card = "ace"

                if next_card in card:
                    result = True

        return result


class DeckTwo(Deck):
    def __init__(self, x, y):
        Deck.__init__(self, x, y)
        self.hidden_cards = []
        self.cards_list = []
        self.x = x

    def clicking_down(self, card):
        if self.check_position() and len(self.cards) > 0:
            pos = pygame.mouse.get_pos()
            c = self.cards.pop()
            card.moved_card.append(c)
            self.cards_list.remove(c)
            card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top)
            card.moved = True
            card.cards = self
            self.rect.left -= 20
        else:
            pos = pygame.mouse.get_pos()
            flag = False
            if 30 <= pos[0] <= 101:
                if 30 <= pos[1] <= 126:
                    flag = True
            if flag:
                self.rect.left = self.x
                if len(self.hidden_cards) > 0:
                    self.cards = []
                    for i in range(1):
                        c = self.hidden_cards.pop()
                        self.cards_list.insert(0, c)
                        self.cards.append(c)
                        if len(self.hidden_cards) == 0 and i < 0:
                            break

                else:
                    self.hidden_cards.extend(self.cards_list)
                    self.cards_list = []
                    self.cards = []

                if len(self.cards) > 1:
                    for i in range(len(self.cards)):
                        if i > 0:
                            self.rect.left += 20

    def draw_the_card(self, screen, card_dict):
        x = self.x
        if len(self.hidden_cards) > 0:
            screen.blit(card_dict["back_side"], [30, 30, 71, 97])
            if len(self.cards_list) > 0 and len(self.cards) > 0:
                for item in self.cards:
                    screen.blit(card_dict[item], [x, self.rect.top])
                    x += 20
        else:
            if len(self.cards_list) > 0 and len(self.cards) > 0:
                for item in self.cards:
                    screen.blit(card_dict[item], [x, self.rect.top])
                    x += 20
            surface_alpha = screen.convert_alpha()
            surface_alpha.fill([0, 0, 0, 0])
            pygame.draw.ellipse(surface_alpha, (255, 255, 255, 64), [40, 40, 60, 60], 5)
            screen.blit(surface_alpha, (0, 0))

    def adding_card(self, card):
        self.cards.extend(card)
        self.cards_list.extend(card)
        self.rect.left += 20


class DeckThree(Deck):
    def checking_card(self, moved_card):
        result = False
        if len(moved_card) == 1:
            card = moved_card[0]
            if len(self.cards) == 0:
                if card[:3] == 'ace':
                    result = True
            else:
                suit = self.cards[0][4:]
                next_card = ''
                if suit in card:
                    if 'ace' in self.cards[-1]:
                        next_card = '2_' + suit
                    elif '2_' in self.cards[-1]:
                        next_card = '3_' + suit
                    elif '3_' in self.cards[-1]:
                        next_card = '4_' + suit
                    elif '4_' in self.cards[-1]:
                        next_card = '5_' + suit
                    elif '5_' in self.cards[-1]:
                        next_card = '6_' + suit
                    elif '6_' in self.cards[-1]:
                        next_card = '7_' + suit
                    elif '7_' in self.cards[-1]:
                        next_card = '8_' + suit
                    elif '8_' in self.cards[-1]:
                        next_card = '9_' + suit
                    elif '9_' in self.cards[-1]:
                        next_card = '10_' + suit
                    elif '10_' in self.cards[-1]:
                        next_card = 'jack_' + suit
                    elif 'jack_' in self.cards[-1]:
                        next_card = 'queen_' + suit
                    elif 'queen_' in self.cards[-1]:
                        next_card = 'king_' + suit

                    if next_card == card:
                        result = True
        return result

    def clicking_down(self, card):
        if self.check_position() and len(self.cards) > 0:
            pos = pygame.mouse.get_pos()
            card.moved_card.append(self.cards.pop())
            card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top)
            card.moved = True
            card.cards = self

    def adding_card(self, card):
        self.cards.extend(card)

    def draw_the_card(self, screen, card_dict):
        surface_alpha = screen.convert_alpha()
        surface_alpha.fill([0, 0, 0, 0])
        pygame.draw.rect(surface_alpha, (255, 255, 255, 64), [self.rect.left, self.rect.top, 71, 96], 2)
        screen.blit(surface_alpha, (0, 0))
        if len(self.cards) > 0:
            screen.blit(card_dict[self.cards[-1]], [self.rect.left, self.rect.top])


def shuffle_cards():
    r = []
    lst = ["ace_clubs", "2_clubs", "3_clubs", "4_clubs", "5_clubs", "6_clubs",
           "7_clubs", "8_clubs", "9_clubs", "10_clubs", "jack_clubs", "queen_clubs",
           "king_clubs", "ace_spades", "2_spades", "3_spades", "4_spades",
           "5_spades", "6_spades", "7_spades", "8_spades", "9_spades", "10_spades",
           "jack_spades", "queen_spades", "king_spades", "ace_hearts", "2_hearts",
           "3_hearts", "4_hearts", "5_hearts", "6_hearts", "7_hearts", "8_hearts",
           "9_hearts", "10_hearts", "jack_hearts", "queen_hearts", "king_hearts",
           "ace_diamonds", "2_diamonds", "3_diamonds", "4_diamonds", "5_diamonds",
           "6_diamonds", "7_diamonds", "8_diamonds", "9_diamonds", "10_diamonds",
           "jack_diamonds", "queen_diamonds", "king_diamonds"]

    length = len(lst)
    for i in range(length):
        if len(lst) > 1:
            c = random.choice(lst)
            r.append(c)
            lst.remove(c)
        else:
            c = lst.pop()
            r.append(c)

    return r


def main():
    pygame.init()

    screen = pygame.display.set_mode([725, 725])

    pygame.display.set_caption("Пасьянс «Косынка»")

    done = False

    clock = pygame.time.Clock()
    card_dict = {}
    img = pygame.image.load("card_images/ace_clubs.png").convert()
    card_dict["ace_clubs"] = img
    img = pygame.image.load("card_images/2_clubs.png").convert()
    card_dict["2_clubs"] = img
    img = pygame.image.load("card_images/3_clubs.png").convert()
    card_dict["3_clubs"] = img
    img = pygame.image.load("card_images/4_clubs.png").convert()
    card_dict["4_clubs"] = img
    img = pygame.image.load("card_images/5_clubs.png").convert()
    card_dict["5_clubs"] = img
    img = pygame.image.load("card_images/6_clubs.png").convert()
    card_dict["6_clubs"] = img
    img = pygame.image.load("card_images/7_clubs.png").convert()
    card_dict["7_clubs"] = img
    img = pygame.image.load("card_images/8_clubs.png").convert()
    card_dict["8_clubs"] = img
    img = pygame.image.load("card_images/9_clubs.png").convert()
    card_dict["9_clubs"] = img
    img = pygame.image.load("card_images/10_clubs.png").convert()
    card_dict["10_clubs"] = img
    img = pygame.image.load("card_images/jack_clubs.png").convert()
    card_dict["jack_clubs"] = img
    img = pygame.image.load("card_images/queen_clubs.png").convert()
    card_dict["queen_clubs"] = img
    img = pygame.image.load("card_images/king_clubs.png").convert()
    card_dict["king_clubs"] = img
    img = pygame.image.load("card_images/ace_spades.png").convert()
    card_dict["ace_spades"] = img
    img = pygame.image.load("card_images/2_spades.png").convert()
    card_dict["2_spades"] = img
    img = pygame.image.load("card_images/3_spades.png").convert()
    card_dict["3_spades"] = img
    img = pygame.image.load("card_images/4_spades.png").convert()
    card_dict["4_spades"] = img
    img = pygame.image.load("card_images/5_spades.png").convert()
    card_dict["5_spades"] = img
    img = pygame.image.load("card_images/6_spades.png").convert()
    card_dict["6_spades"] = img
    img = pygame.image.load("card_images/7_spades.png").convert()
    card_dict["7_spades"] = img
    img = pygame.image.load("card_images/8_spades.png").convert()
    card_dict["8_spades"] = img
    img = pygame.image.load("card_images/9_spades.png").convert()
    card_dict["9_spades"] = img
    img = pygame.image.load("card_images/10_spades.png").convert()
    card_dict["10_spades"] = img
    img = pygame.image.load("card_images/jack_spades.png").convert()
    card_dict["jack_spades"] = img
    img = pygame.image.load("card_images/queen_spades.png").convert()
    card_dict["queen_spades"] = img
    img = pygame.image.load("card_images/king_spades.png").convert()
    card_dict["king_spades"] = img
    img = pygame.image.load("card_images/ace_hearts.png").convert()
    card_dict["ace_hearts"] = img
    img = pygame.image.load("card_images/2_hearts.png").convert()
    card_dict["2_hearts"] = img
    img = pygame.image.load("card_images/3_hearts.png").convert()
    card_dict["3_hearts"] = img
    img = pygame.image.load("card_images/4_hearts.png").convert()
    card_dict["4_hearts"] = img
    img = pygame.image.load("card_images/5_hearts.png").convert()
    card_dict["5_hearts"] = img
    img = pygame.image.load("card_images/6_hearts.png").convert()
    card_dict["6_hearts"] = img
    img = pygame.image.load("card_images/7_hearts.png").convert()
    card_dict["7_hearts"] = img
    img = pygame.image.load("card_images/8_hearts.png").convert()
    card_dict["8_hearts"] = img
    img = pygame.image.load("card_images/9_hearts.png").convert()
    card_dict["9_hearts"] = img
    img = pygame.image.load("card_images/10_hearts.png").convert()
    card_dict["10_hearts"] = img
    img = pygame.image.load("card_images/jack_hearts.png").convert()
    card_dict["jack_hearts"] = img
    img = pygame.image.load("card_images/queen_hearts.png").convert()
    card_dict["queen_hearts"] = img
    img = pygame.image.load("card_images/king_hearts.png").convert()
    card_dict["king_hearts"] = img
    img = pygame.image.load("card_images/ace_diamonds.png").convert()
    card_dict["ace_diamonds"] = img
    img = pygame.image.load("card_images/2_diamonds.png").convert()
    card_dict["2_diamonds"] = img
    img = pygame.image.load("card_images/3_diamonds.png").convert()
    card_dict["3_diamonds"] = img
    img = pygame.image.load("card_images/4_diamonds.png").convert()
    card_dict["4_diamonds"] = img
    img = pygame.image.load("card_images/5_diamonds.png").convert()
    card_dict["5_diamonds"] = img
    img = pygame.image.load("card_images/6_diamonds.png").convert()
    card_dict["6_diamonds"] = img
    img = pygame.image.load("card_images/7_diamonds.png").convert()
    card_dict["7_diamonds"] = img
    img = pygame.image.load("card_images/8_diamonds.png").convert()
    card_dict["8_diamonds"] = img
    img = pygame.image.load("card_images/9_diamonds.png").convert()
    card_dict["9_diamonds"] = img
    img = pygame.image.load("card_images/10_diamonds.png").convert()
    card_dict["10_diamonds"] = img
    img = pygame.image.load("card_images/jack_diamonds.png").convert()
    card_dict["jack_diamonds"] = img
    img = pygame.image.load("card_images/queen_diamonds.png").convert()
    card_dict["queen_diamonds"] = img
    img = pygame.image.load("card_images/king_diamonds.png").convert()
    card_dict["king_diamonds"] = img
    img = pygame.image.load("card_images/back_side.png").convert()
    card_dict["back_side"] = img
    card_list = shuffle_cards()
    deck_list = [DeckTwo(130, 30), DeckOne(30, 160), DeckOne(130, 160), DeckOne(230, 160),
                 DeckOne(330, 160), DeckOne(430, 160), DeckOne(530, 160),
                 DeckOne(630, 160), DeckThree(330, 30), DeckThree(430, 30), DeckThree(530, 30),
                 DeckThree(630, 30)]
    m_card = MovingCard()
    deck_list[1].extend_list(card_list[:1])
    del card_list[:1]
    deck_list[2].extend_list(card_list[:2])
    del card_list[:2]
    deck_list[3].extend_list(card_list[:3])
    del card_list[:3]
    deck_list[4].extend_list(card_list[:4])
    del card_list[:4]
    deck_list[5].extend_list(card_list[:5])
    del card_list[:5]
    deck_list[6].extend_list(card_list[:6])
    del card_list[:6]
    deck_list[7].extend_list(card_list[:7])
    del card_list[:7]

    deck_list[0].hidden_cards.extend(card_list)
    game_over = False
    intro = True

    while intro:

        bg = pygame.image.load("screens/intro.jpg")
        screen.blit(bg, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                m_card.file_handling(m_card.score)
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    m_card.file_handling(m_card.score)
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in deck_list:
                    item.clicking_down(m_card)

            if event.type == pygame.MOUSEBUTTONUP:
                m_card.clicking_up(deck_list)

        for item in deck_list:
            if isinstance(item, DeckThree):
                if len(item.cards) != 13:
                    break
        else:
            game_over = True

        bg = pygame.image.load("screens/background.jpg")
        screen.blit(bg, (0, 0))

        for item in deck_list:
            item.draw_the_card(screen, card_dict)
        m_card.draw(screen, card_dict)

        if game_over:
            bg = pygame.image.load("screens/win_screen.jpg")
            screen.blit(bg, (0, 0))
        m_card.display_score(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
