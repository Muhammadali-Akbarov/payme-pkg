upload:
	./scripts/release.sh


obfuscate:
	pyarmor gen -O ./build/obf -r ./payme/__init__.py
