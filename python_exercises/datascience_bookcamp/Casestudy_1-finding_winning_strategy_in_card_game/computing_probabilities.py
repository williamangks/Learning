#!/usr/bin/env python3

# Defining event conditions
def is_heads_or_tails(outcome): return outcome in {"Heads","Tails"}
def is_neither(outcome): return not is_heads_or_tails(outcome)

# Defining additional event conditions
def is_heads(outcome): return outcome == "Heads"
def is_tails(outcome): return outcome == "Tails"

# Defining an event-detection function
def get_matching_event(event_condition, sample_space):
  return set([outcome for outcome in sample_space
              if event_condition(outcome)])

# Defining function to compute event probabilities
def compute_probability(event_condition, generic_sample_space):
  event = get_matching_event(event_condition, generic_sample_space)
  return len(event) / len(generic_sample_space)

# Defining a generalized event probability function
def compute_event_probability(event_condition, generic_sample_space):
  event = get_matching_event(event_condition, generic_sample_space)
  if type(generic_sample_space) == type(set()):
    return len(event) / len(generic_sample_space)
  
  event_size = sum(generic_sample_space[outcome] for outcome in event)
  return event_size / sum(generic_sample_space.values())


def main():
	# Note: we use sample space approach to probability
  sample_space = {"Heads", "Tails"}
  weighted_sample_space = {"Heads": 4, "Tails": 1} # Representing a weighted sample space
  
  # Probability of a normal coin
  probability_heads = 1 / len(sample_space)
  # print("Probability of choosing heads is {}\n".format(probability_heads))
  assert probability_heads == 0.5

  # Detecting events using event conditions
  event_conditions = [is_heads_or_tails, is_heads, is_tails, is_neither]
  for event_condition in event_conditions:
    print("Event Condition: {}".format(event_condition.__name__))
    event = get_matching_event(event_condition, sample_space)
    print("Event: {}".format(event))

    # Computing event probabilities
    prob = compute_probability(event_condition, sample_space)
    name = event_condition.__name__
    print("Probabilty of event arising from {} is {}".format(name, prob))

    # Computing weighted event probabilities
    prob = compute_event_probability(event_condition, weighted_sample_space)
    name = event_condition.__name__
    print("Probability of event arising from {} is {}\n".format(name, prob))

  # Computing the sample space of children
  possible_children = ["Boy", "Girl"]
  sample_space = set()
  for child1 in possible_children:
    for child2 in possible_children:
      for child3 in possible_children:
        for child4 in possible_children:
          outcome = (child1, child2, child3, child4)
          sample_space.add(outcome)
  
  # Computing the sample space using product
  from itertools import product
  all_combinations = product(*(4 * [possible_children]))
  assert set(all_combinations) == sample_space

  # Passing repeat into product
  sample_space_efficient = set(product(possible_children, repeat = 4))
  assert sample_space == sample_space_efficient

  # Computing the probability of two boys
  def has_two_boys(outcome): return len([child for child in outcome if child == "Boy"]) == 2
  prob = compute_event_probability(has_two_boys, sample_space)
  print("Probability of 2 boys is {}".format(prob))


if __name__ == "__main__":
  main()
