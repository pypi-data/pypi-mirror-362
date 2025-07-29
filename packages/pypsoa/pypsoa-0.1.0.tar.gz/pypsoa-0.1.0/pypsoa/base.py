import random
from typing import List, Tuple, Callable


class Vector:
    """
    A 2D vector class for representing positions and velocities in particle swarm optimization.

    This class provides basic vector operations including addition, subtraction,
    scalar multiplication, and random vector generation within specified bounds.
    """

    def __init__(self, x: float, y: float) -> None:
        """
        Initialize a 2D vector with x and y coordinates.

        Args:
            x: The x-coordinate of the vector
            y: The y-coordinate of the vector
        """
        self.x = x
        self.y = y

    @classmethod
    def random(cls, x_bounds: Tuple[int, int], y_bounds: Tuple[int, int]) -> "Vector":
        """
        Create a random vector within the specified bounds.

        Args:
            x_bounds: Tuple of (min_x, max_x) for x-coordinate bounds
            y_bounds: Tuple of (min_y, max_y) for y-coordinate bounds

        Returns:
            A new Vector instance with random coordinates within the specified bounds
        """
        return cls(
            random.uniform(x_bounds[0], x_bounds[1]),
            random.uniform(y_bounds[0], y_bounds[1]),
        )

    def __sub__(self, other: "Vector") -> "Vector":
        """
        Subtract another vector from this vector.

        Args:
            other: The vector to subtract from this vector

        Returns:
            A new Vector representing the difference
        """
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other: "Vector") -> "Vector":
        """
        Add another vector to this vector.

        Args:
            other: The vector to add to this vector

        Returns:
            A new Vector representing the sum
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vector":
        """
        Multiply this vector by a scalar value.

        Args:
            scalar: The scalar value to multiply the vector by

        Returns:
            A new Vector representing the scaled vector
        """
        return Vector(self.x * scalar, self.y * scalar)

    def __repr__(self) -> str:
        """
        Return a string representation of the vector.

        Returns:
            String representation in the format "Vector(x, y)"
        """
        return f"Vector({self.x}, {self.y})"


class Particle:
    """
    A particle in the particle swarm optimization algorithm.

    Each particle has a position, velocity, fitness value, and personal best position
    and fitness. The particle moves through the search space based on its velocity
    and updates its personal best when it finds a better position.
    """

    def __init__(self, initial_pos: Vector) -> None:
        """
        Initialize a particle with an initial position.

        Args:
            initial_pos: The initial position of the particle in the search space
        """
        self.pos = initial_pos
        self.vel = Vector(0.0, 0.0)
        self.fitness = float("inf")
        self.p_best = (self.pos, self.fitness)

    def update_fitness(self, fitness: float) -> None:
        """
        Update the particle's fitness and personal best if the new fitness is better.

        Args:
            fitness: The new fitness value to evaluate
        """
        if fitness < self.p_best[1]:
            self.p_best = (self.pos, fitness)
        self.fitness = fitness


class Swarm:
    """
    A swarm of particles for particle swarm optimization.

    The swarm manages a collection of particles and implements the PSO algorithm
    including fitness evaluation, particle movement, and global best tracking.
    """

    def __init__(
        self,
        particles: List[Particle],
        w: float = 0.5,
        c1: float = 1.0,
        c2: float = 2.0,
        velocity_factor: float = 0.1,
    ) -> None:
        """
        Initialize a swarm with particles and PSO parameters.

        Args:
            particles: List of particles in the swarm
            w: Inertia weight for velocity update (default: 0.5)
            c1: Cognitive learning factor for personal best influence (default: 1.0)
            c2: Social learning factor for global best influence (default: 2.0)
            velocity_factor: Scaling factor for velocity updates (default: 0.1)
        """
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.velocity_factor = velocity_factor
        self.particles = particles
        self.g_best = self.particles[0].p_best

    @classmethod
    def from_bounds(
        cls,
        num_particles: int,
        x_bounds: Tuple[int, int],
        y_bounds: Tuple[int, int],
        **kwargs,
    ) -> "Swarm":
        """
        Create a swarm with randomly positioned particles within specified bounds.

        Args:
            num_particles: Number of particles to create in the swarm
            x_bounds: Tuple of (min_x, max_x) for x-coordinate bounds
            y_bounds: Tuple of (min_y, max_y) for y-coordinate bounds
            **kwargs: Additional keyword arguments to pass to the Swarm constructor

        Returns:
            A new Swarm instance with randomly positioned particles
        """
        particles = [
            Particle(Vector.random(x_bounds, y_bounds)) for _ in range(num_particles)
        ]
        return cls(particles, **kwargs)

    def eval(self, fit_func: Callable[[Vector], float]) -> None:
        """
        Evaluate the fitness of all particles and update global best.

        Args:
            fit_func: Function that takes a Vector position and returns a fitness value
        """
        for particle in self.particles:
            d = fit_func(particle.pos)
            particle.update_fitness(d)
            if particle.p_best[1] < self.g_best[1]:
                self.g_best = particle.p_best

    def step(self) -> None:
        """
        Perform one step of the particle swarm optimization algorithm.

        Updates each particle's velocity and position based on personal best,
        global best, and current velocity using the PSO update equations.
        """
        for particle in self.particles:
            v1 = (particle.p_best[0] - particle.pos) * self.c1 * random.random()
            v2 = (self.g_best[0] - particle.pos) * self.c2 * random.random()
            particle.vel = (v1 + v2 + particle.vel * self.w) * self.velocity_factor
            particle.pos = particle.pos + particle.vel

    def get_positions(self) -> Tuple[List[float], List[float]]:
        """
        Get the current positions of all particles in the swarm.

        Returns:
            Tuple containing (x_coordinates, y_coordinates) as separate lists
        """
        x_vals = [p.pos.x for p in self.particles]
        y_vals = [p.pos.y for p in self.particles]
        return x_vals, y_vals
