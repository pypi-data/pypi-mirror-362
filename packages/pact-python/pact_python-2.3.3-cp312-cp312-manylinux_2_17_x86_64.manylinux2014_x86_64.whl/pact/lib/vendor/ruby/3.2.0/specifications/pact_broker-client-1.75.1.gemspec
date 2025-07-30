# -*- encoding: utf-8 -*-
# stub: pact_broker-client 1.75.1 ruby lib

Gem::Specification.new do |s|
  s.name = "pact_broker-client".freeze
  s.version = "1.75.1"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Beth Skurrie".freeze]
  s.date = "2023-12-07"
  s.description = "Client for the Pact Broker. Publish, retrieve and query pacts and verification results. Manage webhooks and environments.".freeze
  s.email = ["beth@bethesque.com".freeze]
  s.executables = ["pact-broker".freeze, "pactflow".freeze]
  s.files = ["bin/pact-broker".freeze, "bin/pactflow".freeze]
  s.homepage = "https://github.com/pact-foundation/pact_broker-client.git".freeze
  s.licenses = ["MIT".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 2.0".freeze)
  s.rubygems_version = "3.4.19".freeze
  s.summary = "See description".freeze

  s.installed_by_version = "3.4.19" if s.respond_to? :installed_by_version

  s.specification_version = 4

  s.add_runtime_dependency(%q<httparty>.freeze, [">= 0.21.0", "< 1.0.0"])
  s.add_runtime_dependency(%q<term-ansicolor>.freeze, ["~> 1.7"])
  s.add_runtime_dependency(%q<table_print>.freeze, ["~> 1.5"])
  s.add_runtime_dependency(%q<thor>.freeze, [">= 0.20", "< 2.0"])
  s.add_runtime_dependency(%q<rake>.freeze, ["~> 13.0"])
  s.add_runtime_dependency(%q<dig_rb>.freeze, ["~> 1.0"])
end
