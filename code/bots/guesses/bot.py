from nltk.corpus import wordnet
from colorama import Fore, Style

class bot:
    def __init__(self, board):
        self.board = board
        self.probability_scores_0 = {tile.word: 0 for tile in board}
        self.probability_scores_1 = {tile.word: 0 for tile in board}

    def normalize_list(self, lst):
        """
        Normalize a list of values between 0 and 1.
        """
        min_val = min(lst)
        max_val = max(lst)
        return [(x - min_val) / (max_val - min_val) for x in lst] if max_val != min_val else [0.5] * len(lst)

    def nltk_word_similarity(self, word1, word2):
        """
        Calculate similarity between two words using WordNet's Wu-Palmer Similarity.
        """
        if word1 is None or word2 is None:
            return 0
        synsets1 = wordnet.synsets(word1)
        synsets2 = wordnet.synsets(word2)

        if synsets1 and synsets2:
            similarity = max(
                (synset1.wup_similarity(synset2) or 0)
                for synset1 in synsets1
                for synset2 in synsets2
            )
            return similarity
        else:
            return 0

    def guess(self, clue, related):
        """
        Guess the most likely 'n' words based on the clue.
        
        Args:
            clue (str): The clue word given to the player.
            related (int): The number of most likely words to return.
        
        Returns:
            list: A list of 'related' most likely words based on their similarity to the clue.
        """
        current_team_scores = (
            self.probability_scores_0
            if self.board.turn == 0
            else self.probability_scores_1
        )

        for tile in self.board:
            if tile.used:
                current_team_scores[tile.word] = 0
            else:
                similarity = self.nltk_word_similarity(clue, tile.word)
                current_team_scores[tile.word] = similarity

        # Normalize the similarity scores
        normalized_scores = self.normalize_list(list(current_team_scores.values()))

        # Update scores with normalized values
        for word, normalized_score in zip(current_team_scores.keys(), normalized_scores):
            current_team_scores[word] = normalized_score

        # Sort and return top 'related' words
        sorted_words = sorted(
            current_team_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )
        most_likely_words = [word for word, score in sorted_words[:related]]
        return most_likely_words

    def update_bot(self, board):
        """
        Update the board and reset probabilities for used words only. 
        EDIT: I have updated this function to discount words from previous turns to stop the bot from making erronueous guesses based on multiple low percent words
        """
        self.board = board
        for tile in self.board:
            if tile.used:
                self.probability_scores_0[tile.word] = 0
                self.probability_scores_1[tile.word] = 0
            else:
                self.probability_scores_0[tile.word] = 3/4 * self.probability_scores_0[tile.word]
                self.probability_scores_1[tile.word] = 3/4 * self.probability_scores_0[tile.word]               

    def toString(self):
        """
        Generate string representations of two 5x5 boards (one for each team) showing the
        probability of each word being related to the respective team. Each word is color-coded
        for readability.
        
        Returns:
            str: The formatted string representation of the boards.
        """
        color_map = {
            0: Fore.RED,    # Red team
            1: Fore.BLUE,   # Blue team
            2: Fore.YELLOW, # Neutral (Tan)
            -1: Fore.BLACK, # Assassin
            "reset": Style.RESET_ALL,
        }
        
        def format_board(scores, color_map):
            board_lines = []
            row = []
            for idx, tile in enumerate(self.board):  # Use direct iteration
                color = color_map.get(tile.team, Style.RESET_ALL)
                probability = scores.get(tile.word, 0)
                row.append(f"{color}{tile.word} ({probability:.2f}){color_map['reset']}")
                if (idx + 1) % 5 == 0:  # After every 5 tiles, create a row
                    board_lines.append(" | ".join(row))
                    row = []
            return "\n".join(board_lines)

        # Generate the boards for both teams
        red_team_board = f"{Fore.RED}RED TEAM BOARD:{Style.RESET_ALL}\n{format_board(self.probability_scores_0, color_map)}"
        blue_team_board = f"{Fore.BLUE}BLUE TEAM BOARD:{Style.RESET_ALL}\n{format_board(self.probability_scores_1, color_map)}"
        
        # Concatenate boards with a separator and return
        return f"{red_team_board}\n\n{'-' * 80}\n\n{blue_team_board}\n\n{'-' * 80}\n\n"
    
    def get_probability(self, tile):
        """
        Retrieve the probability score of a given tile based on the current team's turn.

        Args:
            tile (Tile): The tile whose probability score is being queried.

        Returns:
            float: The probability score for the tile.
        """
        current_team_scores = (
            self.probability_scores_0 if self.board.turn == 0 else self.probability_scores_1
        )
        return current_team_scores.get(tile.word, 0)


