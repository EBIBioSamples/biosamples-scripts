from mongo_connector import MongoConnector


ACCESSION_FILE_PATH = "../resources/accessions_to_migrate_domain.txt"

def main():
    domain_migrator = DomainMigrator()
    # domain_migrator.migrate_domain('SAMEA671223413', 'self.FakeDomain', 'self.MyDomain')
    # domain_migrator.migrate_domains(['SAMEA6712333', 'SAMEA671223413'], '', 'self.biosampleCuration2')
    domain_migrator.migrate_all_in_file(ACCESSION_FILE_PATH, 'subs.team-41', 'self.BioSamplesMigration')
    # domain_migrator.migrate_all_from_old_to_new('76330293e830ea8a0decaa0bbcc0c85d4e53c3ef3e6bf317efc29cfb11f2baea', 'subs.team-41')
    # domain_migrator.migrate_all_from_old_to_new('subs.team-34', 'self.team-34')


class DomainMigrator:
    def __init__(self):
        self.mongo_connector = MongoConnector()

    def migrate_all_in_file(self, accession_file_path, old_domain, new_domain):
        accession_list = self.get_accessions(accession_file_path)
        self.migrate_domains(accession_list, old_domain, new_domain)
        print("Migrated " + str(len(accession_list)) + " samples")

    def migrate_all_from_old_to_new(self, old_domain, new_domain):
        samples = self.mongo_connector.get_samples({'domain': old_domain})
        for sample in samples:
            accession = sample['_id']
            self.migrate_domain(accession, old_domain, new_domain)

    def migrate_domains(self, accessions, old_domain, new_domain):
        for accession in accessions:
            self.migrate_domain(accession, old_domain, new_domain)

    def migrate_domain(self, accession, old_domain, new_domain):
        domain_in_db = self.mongo_connector.get_sample(accession)['domain']
        if not old_domain or old_domain == domain_in_db:
            self.mongo_connector.update_sample(accession, 'domain', new_domain)
            print("Domain migrated for sample : " + accession)
        else:
            print("DOMAIN MISMATCH for " + accession + " : expected = " + old_domain + ", actual = " + domain_in_db)

    @staticmethod
    def get_accessions(accessions_file_path):
        print("Reading accessions from: " + accessions_file_path)
        with open(accessions_file_path) as f:
            accessions = f.read().splitlines()
        return accessions


if __name__ == '__main__':
    main()
