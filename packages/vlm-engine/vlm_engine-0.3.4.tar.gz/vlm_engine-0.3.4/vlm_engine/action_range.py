"""
Represents the search range for a specific action with dual boundary detection
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class ActionRange:
    """Represents the search range for a specific action with dual boundary detection"""
    start_frame: int
    end_frame: int
    action_tag: str
    confirmed_present: bool = False
    confirmed_absent: bool = False

    # Dual boundary tracking
    start_found: Optional[int] = None  # Confirmed start frame
    end_found: Optional[int] = None    # Confirmed end frame
    end_search_start: Optional[int] = None  # Start of end search range
    end_search_end: Optional[int] = None    # End of end search range
    searching_end: bool = False  # Flag for end search mode
    added: bool = False  # Whether this range has been added to segments
    stall_count: int = 0
    is_stalled: bool = False
    last_midpoint: Optional[int] = None
    
    # Per-action depth tracking
    max_depth: Optional[int] = None
    current_depth: int = 0
    
    def __post_init__(self):
        """Calculate initial max depth after initialization"""
        self._calculate_max_depth()

    def is_resolved(self) -> bool:
        """Check if this action search is complete."""
        if self.confirmed_absent:
            return True
        
        # If searching for the end, resolution now depends on the search range crossing over.
        if self.searching_end:
            if self.end_search_start is not None and self.end_search_end is not None:
                if self.end_search_start > self.end_search_end:
                    return True
        
        # Original conditions for start search resolution and stalling still apply.
        if self.confirmed_present and self.end_found is not None:
            return True
        if (self.start_frame > self.end_frame) and not self.searching_end:
            return True
            
        return self.is_stalled

    def get_start_midpoint(self) -> Optional[int]:
        """Get the midpoint frame for start boundary search"""
        if self.start_found is not None or self.confirmed_absent:
            return None
        if self.start_frame >= self.end_frame:
            return None
        return (self.start_frame + self.end_frame) // 2

    def get_end_midpoint(self) -> Optional[int]:
        """Get the midpoint frame for end boundary search"""
        if not self.searching_end or self.end_found is not None:
            return None
        if self.end_search_start is None or self.end_search_end is None:
            return None
        if self.end_search_start >= self.end_search_end:
            return None
        return (self.end_search_start + self.end_search_end) // 2

    def get_midpoint(self) -> Optional[int]:
        """Get the next midpoint frame for binary search (prioritizes end search)"""
        end_midpoint = self.get_end_midpoint()
        if end_midpoint is not None:
            return end_midpoint
        return self.get_start_midpoint()

    def initiate_end_search(self, total_frames: int) -> None:
        """Initialize end frame search after start frame is found"""
        if self.start_found is not None and not self.searching_end:
            self.searching_end = True
            self.end_search_start = self.start_found
            self.end_search_end = total_frames - 1
            # Recalculate max depth for end search
            self._calculate_max_depth()
    
    def _calculate_max_depth(self) -> None:
        """Calculate max depth based on current search range"""
        import math
        
        if self.searching_end and self.end_search_start is not None and self.end_search_end is not None:
            # Calculate depth for end search range
            search_range = self.end_search_end - self.end_search_start + 1
        else:
            # Calculate depth for start search range
            search_range = self.end_frame - self.start_frame + 1
        
        if search_range > 0:
            # self.max_depth = math.ceil(math.log2(search_range)) + 2
            self.max_depth = max(1, math.floor(math.log2(search_range) * 0.5))
        else:
            self.max_depth = 1
    
    def increment_depth(self) -> None:
        """Increment the current depth counter"""
        self.current_depth += 1
    
    def has_reached_max_depth(self) -> bool:
        """Check if this action has reached its maximum depth"""
        return self.max_depth is not None and self.current_depth >= self.max_depth
    
    def reset_depth_for_end_search(self) -> None:
        """Reset depth counter when transitioning to end search"""
        self.current_depth = 0
        self._calculate_max_depth()
