import Mathlib

namespace Nonassoc

universe u

/-- A magma has a binary multiplication, with no associativity assumptions. -/
class Magma (α : Type u) extends Mul α

/-- Left division operation `ldiv a b`, intended as the solution to `a * x = b`. -/
class LeftDiv (α : Type u) where
  ldiv : α → α → α

/-- Right division operation `rdiv b a`, intended as the solution to `x * a = b`. -/
class RightDiv (α : Type u) where
  rdiv : α → α → α

/-- Convenience alias for the left-division operation. -/
abbrev ldiv {α : Type u} [LeftDiv α] : α → α → α := LeftDiv.ldiv
/-- Convenience alias for the right-division operation. -/
abbrev rdiv {α : Type u} [RightDiv α] : α → α → α := RightDiv.rdiv

/--
A quasigroup is a magma where both left and right division solve multiplication
equations on the nose.
-/
class Quasigroup (α : Type u) extends Magma α, LeftDiv α, RightDiv α where
  mul_left_div : ∀ a b : α, a * ldiv a b = b
  left_div_mul : ∀ a b : α, ldiv a (a * b) = b
  mul_right_div : ∀ a b : α, rdiv b a * a = b
  right_div_mul : ∀ a b : α, rdiv (b * a) a = b

/-- A loop is a quasigroup with a two-sided multiplicative identity. -/
class Loop (α : Type u) extends Quasigroup α, One α where
  one_mul : ∀ a : α, 1 * a = a
  mul_one : ∀ a : α, a * 1 = a

section QuasigroupLemmas

variable {α : Type u} [Quasigroup α]

-- Basic simplification lemmas re-exposing quasigroup axioms.
@[simp] theorem mul_ldiv (a b : α) : a * ldiv a b = b :=
  Quasigroup.mul_left_div a b

@[simp] theorem ldiv_mul (a b : α) : ldiv a (a * b) = b :=
  Quasigroup.left_div_mul a b

@[simp] theorem mul_rdiv (a b : α) : rdiv b a * a = b :=
  Quasigroup.mul_right_div a b

@[simp] theorem rdiv_mul (a b : α) : rdiv (b * a) a = b :=
  Quasigroup.right_div_mul a b

end QuasigroupLemmas

section LoopLemmas

variable {α : Type u} [Loop α]

-- Basic simplification lemmas re-exposing loop axioms.
@[simp] theorem one_mul' (a : α) : (1 : α) * a = a :=
  Loop.one_mul a

@[simp] theorem mul_one' (a : α) : a * (1 : α) = a :=
  Loop.mul_one a

@[simp] theorem one_ldiv (a : α) : ldiv (1 : α) a = a := by
  simpa [one_mul'] using (ldiv_mul (a := (1 : α)) (b := a))

@[simp] theorem one_rdiv (a : α) : rdiv a (1 : α) = a := by
  simpa [mul_one'] using (rdiv_mul (a := (1 : α)) (b := a))

end LoopLemmas

end Nonassoc
