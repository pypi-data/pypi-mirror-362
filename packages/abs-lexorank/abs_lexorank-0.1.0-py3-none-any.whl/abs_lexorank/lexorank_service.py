
class LexoRank:
    """
    Dynamic LexoRank implementation that allows for variable rank lengths and spacing.
    - Uses base-62 (0-9, A-Z, a-z)
    - Starts with 5-length ranks, increases length as needed
    - Default bulk rank generation start at 20% of the available rank space
    - Default spacing is 1,00,000 ranks between each rank
    - Can be configured to use different alphabet, min/max lengths, and spacing

    Args:
        alphabet: str (Is is a default alphabet to generate ranks)
        min_length: int (Is is a minimum length of a rank)
        max_length: int (Is is a maximum length of a rank)
        default_spacing: int (Is is a default spacing between ranks)
        rebalancing_diff: int (Is is a min diff between two ranks to rebalance)
        start_from: int (Is is a start point (In percentage) from where we start generate ranks from the available space)
        end_at: int (Is is a end point (In percentage) to where we end generate ranks from the available space)
    """

    def __init__(self, 
                 alphabet:str='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                 min_length:int=5,
                 max_length:int=50,
                 default_spacing:int=1_000_000,
                 rebalancing_diff:int=1,
                 start_from:int=10,
                 end_at:int=60,
                 ):
        self.alphabet = alphabet
        self.base = len(alphabet)
        self.min_length = min_length
        self.max_length = max_length
        self.default_spacing = default_spacing
        self.start_from = start_from
        self.start_val = (self.base ** self.min_length * self.start_from) // 100
        self.end_at = end_at
        self.rebalancing_diff = rebalancing_diff
        self.char_to_val = {c: i for i, c in enumerate(alphabet)}
        self.val_to_char = {i: c for i, c in enumerate(alphabet)}

    def _pad(self, s:str, length:int):
        return s + self.alphabet[0] * (length - len(s))

    def _rank_to_int(self, rank:str):
        val = 0
        for c in rank:
            if c not in self.char_to_val:
                raise ValueError(f"Invalid character '{c}' in rank")
            val = val * self.base + self.char_to_val[c]
        return val

    def _int_to_rank(self, val: int, length: int = None):
        s = []
        # Always convert at least once (for val=0)
        while val > 0 or not s:
            val, r = divmod(val, self.base)
            s.append(self.val_to_char[r])
        rank = ''.join(reversed(s))
        if length is not None:
            rank = rank.rjust(length, self.alphabet[0])
        return rank
    
    def _dynamic_gap(self, rank_length: int) -> int:
        base_gap = self.default_spacing
        # For each character above min_length, double the gap
        return base_gap * (2 ** (rank_length - self.min_length))

    
    def between(self, prev: str = None, next: str = None, spacing: str= None):
        """
        Returns (new_rank, needs_rebalance)
        - new_rank: the generated rank between prev and next
        - needs_rebalance: True if the new rank's length exceeds max_length or if no space is left
        """
        if not prev and not next:
            rank = self._int_to_rank(self.start_val)
            return rank, len(rank) > self.max_length
        
        gap = spacing if spacing else self.default_spacing

        if not next:
            rank_length = len(prev)
            rank_value = self._rank_to_int(prev) + gap
            max_val = self.base ** rank_length
            if rank_value >= max_val:
                # Fallback: generate between prev and max_rank (may extend length)
                max_rank = self._int_to_rank(max_val - 1, rank_length)
                return self.between(prev, max_rank)
            new_rank = self._int_to_rank(rank_value)
            return new_rank, len(new_rank) > self.max_length

        if not prev:
            rank_value = self._rank_to_int(next) - gap
            if rank_value < 0:
                # Fallback: generate between start and next, which may extend length
                rank_length = len(next)
                start_val = (self.base ** rank_length * self.start_from) // 100
                start_rank = self._int_to_rank(start_val, rank_length)
                # Use the between logic for more space (may extend length)
                return self.between(start_rank, next)
            new_rank = self._int_to_rank(rank_value)
            return new_rank, len(new_rank) > self.max_length

        max_len = max(len(prev), len(next))
        for pad_len in range(max_len, max_len + 10):  # Allow rank to grow
            prev_pad = self._pad(prev, pad_len)
            next_pad = self._pad(next, pad_len)

            prev_val = self._rank_to_int(prev_pad)
            next_val = self._rank_to_int(next_pad)

            if next_val - prev_val > self.rebalancing_diff:
                mid_val = (prev_val + next_val) // 2
                rank = self._int_to_rank(mid_val, pad_len)
                needs_rebalance = pad_len > self.max_length
                return rank, needs_rebalance

        # If we reach here, we couldn't find space within allowed growth
        return None, True
    
    def create_initial_rank(self):
        return self.between()
    
    def create_previous_rank(self, rank:str):
        if not rank:
            raise ValueError("Rank is required")
        return self.between(next=rank)
    
    def create_next_rank(self, rank:str):
        if not rank:
            raise ValueError("Rank is required")
        return self.between(prev=rank)

    def generate_bulk(self, count:int = 0, rank_length:int = 0, gap:int = 0, start_rank:str=None):
        """
        Generate `count` ranks of `rank_length` characters.
        Starts from 20% of the available space and adds a fixed gap.
        """
        if not rank_length :
            rank_length = self.min_length

        if not gap:
            gap = self.default_spacing

        max_val = self.base ** rank_length

        if start_rank:
            start_val = self._rank_to_int(start_rank)
        else:
            start_val = (max_val * self.start_from) // 100

        usable_space = max_val - start_val

        if gap is None:
            gap = usable_space // (count + 1)

        if gap == 0:
            raise ValueError("Gap is too small for the given count and rank length")

        ranks = []
        for i in range(count):
            val = start_val + (i + 1) * gap
            rank = self._int_to_rank(val, rank_length)
            ranks.append(rank)

        return ranks
    

    def generate_evenly_bulk(self, count: int = 0, rank_length: int = 0):
        """
        Generate `count` ranks of `rank_length` characters, evenly distributed between
        self.start_from% and self.end_at% of the available space.
        """
        if not rank_length:
            rank_length = self.min_length

        max_val = self.base ** rank_length
        start_val = (max_val * self.start_from) // 100
        end_val = (max_val * self.end_at) // 100

        usable_space = end_val - start_val

        if count <= 0 or usable_space <= count:
            raise ValueError("Not enough space or invalid count")

        gap = usable_space // (count + 1)
        ranks = []
        for i in range(count):
            val = start_val + (i + 1) * gap
            rank = self._int_to_rank(val, rank_length)
            ranks.append(rank)

        return ranks

        