import mathlib

class skewbrace (G : Type*) where
  mul₁ : G → G → G
  one₁ : G
  inv₁ : G → G
  mul_assoc₁ : ∀ a b c : G, mul₁ (mul₁ a b) c = mul₁ a (mul₁ b c)
  one_mul₁   : ∀ a : G, mul₁ one₁ a = a
  mul_one₁   : ∀ a : G, mul₁ a one₁ = a
  mul_left_inv₁ : ∀ a : G, mul₁ (inv₁ a) a = one₁

  mul₂ : G → G → G
  one₂ : G
  inv₂ : G → G
  mul_assoc₂ : ∀ a b c : G, mul₂ (mul₂ a b) c = mul₂ a (mul₂ b c)
  one_mul₂   : ∀ a : G, mul₂ one₂ a = a
  mul_one₂   : ∀ a : G, mul₂ a one₂ = a
  mul_left_inv₂ : ∀ a : G, mul₂ (inv₂ a) a = one₂

  Brace_relations: ∀ a b c : G , mul₁ a (mul₂ b c) = mul₁ (mul₁ (mul₁ a b) (inv₁ a)) (mul₁ a c)

namespace Myskewbrace

variable {G : Type*} [skewbrace G]

-- First law as additive notation
instance : Add G := ⟨skewbrace.mul₁⟩
instance : Zero G := ⟨skewbrace.one₁⟩
instance : Neg G := ⟨skewbrace.inv₁⟩

-- Second law as multiplicative notation
instance : Mul G := ⟨skewbrace.mul₂⟩
instance : One G := ⟨skewbrace.one₂⟩
instance : Inv G := ⟨skewbrace.inv₂⟩
