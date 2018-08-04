from model_mommy import mommy

mommy.generators.add('autoslug.fields.AutoSlugField', mommy.random_gen.gen_slug)
