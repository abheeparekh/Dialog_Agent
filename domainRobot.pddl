(define (domain Dialog)
  (:requirements :strips :typing)
  (:types variable)
  (:predicates 
		   (can_walk ?x - variable)
		   (has_left_leg ?x - variable)
		   (has_right_leg ?x - variable)
		   (can_listen ?x - variable)
		   (can_dance ?x - variable)
	       )

 
  (:action behavior_s0s1
	     :parameters (?x - variable)
	     :precondition (and (has_left_leg ?x) (has_right_leg ?x) )
	     :effect
	     (and (can_walk ?x)
		   ))

  (:action behavior_s0s1s2
	     :parameters (?x - variable)
	     :precondition (and (has_left_leg ?x) (has_right_leg ?x) (can_listen ?x) )
	     :effect
	     (and (can_dance ?x)
		   ))
		 
   
)
