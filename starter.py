import scrabble

scrb = scrabble.Scrabble()
scrb.create_board(dim=15)
scrb.get_solutions()
scrb.validate_solutions(["gig", "streu", "ihr", "treu", "are"])
