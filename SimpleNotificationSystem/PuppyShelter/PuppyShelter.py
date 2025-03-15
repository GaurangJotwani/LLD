from abc import ABC, abstractmethod
from typing import List

# Define the Puppy class with basic attributes.
class Puppy:
    def __init__(self, name: str, age: int, weight: float, breed: str, vaccinated: bool):
        self.name = name
        self.age = age          # Age in months
        self.weight = weight    # Weight in pounds (or kg)
        self.breed = breed
        self.vaccinated = vaccinated

    def __repr__(self):
        return f"Puppy(name={self.name}, age={self.age}, weight={self.weight}, breed={self.breed}, vaccinated={self.vaccinated})"


# AcceptancePolicy interface (or specification)
class AcceptancePolicy(ABC):
    @abstractmethod
    def is_acceptable(self, puppy: Puppy) -> bool:
        pass


# Concrete policy: Accept only puppies above a minimum age.
class MinimumAgePolicy(AcceptancePolicy):
    def __init__(self, min_age: int):
        self.min_age = min_age

    def is_acceptable(self, puppy: Puppy) -> bool:
        return puppy.age >= self.min_age


# Concrete policy: Accept only vaccinated puppies.
class VaccinationPolicy(AcceptancePolicy):
    def is_acceptable(self, puppy: Puppy) -> bool:
        return puppy.vaccinated


# Concrete policy: Accept puppies within a specific weight range (optional).
class MaxWeightPolicy(AcceptancePolicy):
    def __init__(self, max_weight: float):
        self.max_weight = max_weight

    def is_acceptable(self, puppy: Puppy) -> bool:
        return puppy.weight <= self.max_weight


# Composite policy to combine multiple conditions.
class CompositePolicy(AcceptancePolicy):
    def __init__(self, policies: List[AcceptancePolicy]):
        self.policies = policies

    def is_acceptable(self, puppy: Puppy) -> bool:
        return all(policy.is_acceptable(puppy) for policy in self.policies)


# The PuppyShelter class uses a given AcceptancePolicy to decide on acceptance.
class PuppyShelter:
    def __init__(self, acceptance_policy: AcceptancePolicy):
        self.acceptance_policy = acceptance_policy
        self.puppies = []  # Store accepted puppies

    def accept_puppy(self, puppy: Puppy) -> bool:
        """
        Evaluate the puppy with the acceptance policy.
        If accepted, add it to the shelter and return True.
        Otherwise, return False.
        """
        if self.acceptance_policy.is_acceptable(puppy):
            self.puppies.append(puppy)
            print(f"Accepted: {puppy}")
            return True
        else:
            print(f"Rejected: {puppy}")
            return False

    def __repr__(self):
        return f"PuppyShelter(accepted_puppies={self.puppies})"


# Example usage:
if __name__ == "__main__":
    # Define some puppies.
    puppy1 = Puppy("Buddy", 6, 15.0, "Labrador", vaccinated=True)
    puppy2 = Puppy("Lucy", 3, 8.0, "Beagle", vaccinated=False)
    puppy3 = Puppy("Max", 5, 12.0, "Poodle", vaccinated=True)
    puppy4 = Puppy("Bella", 2, 9.0, "Bulldog", vaccinated=True)

    # Define acceptance criteria:
    # - Minimum age of 4 months.
    # - Must be vaccinated.
    # Optionally, you could add a weight limit with MaxWeightPolicy.
    policy = CompositePolicy([
        MinimumAgePolicy(min_age=4),
        VaccinationPolicy(),
        # Uncomment the next line to enforce a weight policy.
        # MaxWeightPolicy(max_weight=14.0)
    ])

    # Create the shelter with the composite policy.
    shelter = PuppyShelter(acceptance_policy=policy)

    # Attempt to add puppies to the shelter.
    shelter.accept_puppy(puppy1)  # Expected: Accepted
    shelter.accept_puppy(puppy2)  # Expected: Rejected (too young and not vaccinated)
    shelter.accept_puppy(puppy3)  # Expected: Accepted
    shelter.accept_puppy(puppy4)  # Expected: Rejected (too young)

    print("\nFinal Shelter State:")
    print(shelter)
