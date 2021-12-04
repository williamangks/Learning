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
  print("Probability of choosing heads is {}\n".format(probability_heads))

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



if __name__ == "__main__":
  main()
