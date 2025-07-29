/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Dialect Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|* From: GradientOps.td                                                       *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace catalyst {
namespace gradient {

class GradientDialect : public ::mlir::Dialect {
  explicit GradientDialect(::mlir::MLIRContext *context);

  void initialize();
  friend class ::mlir::MLIRContext;
public:
  ~GradientDialect() override;
  static constexpr ::llvm::StringLiteral getDialectNamespace() {
    return ::llvm::StringLiteral("gradient");
  }
};
} // namespace gradient
} // namespace catalyst
MLIR_DECLARE_EXPLICIT_TYPE_ID(::catalyst::gradient::GradientDialect)
