from instances import Instances

if __name__ == "__main__":
    Instances = Instances()
    Instances.setup()
    open("key", "w").write(Instances.key["KeyMaterial"])
    print("Instances running...")
    input("Press Enter to terminate instances...")
    Instances.teardown()
