exports.postTransform = function (model) {
  if (model.namespace && model.namespace.uid) {
    // Resolve the complete namespace through DocFX. Its empty parent namespaces
    // may have no generated pages, so linking each segment can produce 404s.
    model.namespace.specName = [{
      lang: 'csharp',
      value: '<xref uid="' + model.namespace.uid + '" displayProperty="fullName"/>'
    }];
  }
  return model;
};
