import Nonassoc.Basic

namespace Nonassoc

universe u

section

variable {α : Type u} [Quasigroup α]

-- In a quasigroup, left-multiplication by `a` has a unique solution.
theorem existsUnique_leftMul_eq (a b : α) : ∃! x : α, a * x = b := by
  refine ⟨ldiv a b, ?_, ?_⟩
  · simp [mul_ldiv]
  · intro y hy
    have h : ldiv a (a * y) = ldiv a b := by simp [hy]
    simpa using h

-- In a quasigroup, right-multiplication by `a` has a unique solution.
theorem existsUnique_rightMul_eq (a b : α) : ∃! x : α, x * a = b := by
  refine ⟨rdiv b a, ?_, ?_⟩
  · simp [mul_rdiv]
  · intro y hy
    have h : rdiv (y * a) a = rdiv b a := by simp [hy]
    simpa using h

end

end Nonassoc
