from mongo_connector import MongoConnector


class DomainMigrator:
    def __init__(self):
        self.mongo_connector = MongoConnector()

    def migrate_all_in_file(self, accession_file_path, old_domain, new_domain):
        accession_list = self.get_accessions(accession_file_path)
        self.migrate_domains(accession_list, old_domain, new_domain)
        print("Migrated " + str(len(accession_list)) + " samples")

    def migrate_all_from_old_to_new(self, old_domain, new_domain):
        samples = self.mongo_connector.get_sample({'domain': old_domain})
        for sample in samples:
            self.migrate_domain(sample['_id'], old_domain, new_domain)

    def migrate_domains(self, accessions, old_domain, new_domain):
        for accession in accessions:
            self.migrate_domain(accession, old_domain, new_domain)

    def migrate_domain(self, accession, old_domain, new_domain):
        domain_in_db = self.mongo_connector.get_sample(accession)['domain']
        if not old_domain or old_domain == domain_in_db:
            self.mongo_connector.update_sample(accession, 'domain', new_domain)
        else:
            print("DOMAIN MISMATCH for " + accession + " : expected = " + old_domain + ", actual = " + domain_in_db)

    @staticmethod
    def get_accessions(accessions_file_path):
        print("Reading accessions from: " + accessions_file_path)
        with open(accessions_file_path) as f:
            accessions = f.read().splitlines()
        return accessions


if __name__ == '__main__':
    domain_migrator = DomainMigrator()
    # domain_migrator.migrate_domain('SAMEA671223413', 'self.1234sdfsf', 'self.biosampleCuration')
    # domain_migrator.migrate_domains(['SAMEA6712333', 'SAMEA671223413'], None, 'self.biosampleCuration2')
    domain_migrator.migrate_all_in_file('../resources/accessions_to_migrate_domain.txt', 'self.BioSamplesMigration', 'self.3a7d2d8567da810952358e87c0fb9fe63f694f1bd4786e8a25a08cd406ed133a')