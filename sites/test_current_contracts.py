"""Guard the current central contract against known documentation regressions."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CurrentContracts(unittest.TestCase):
    def test_email_flows_include_all_supported_proof_pairs(self):
        for name in ('auth/onboarding/onboarding-flow.md',
                     'auth/onboarding/email-confirmation/flow.md',
                     'auth/onboarding/email-confirmation/aws.md',
                     'docs/agents/journeys.md'):
            with self.subTest(path=name):
                text = (ROOT / name).read_text()
                for pair in ('A+B', 'A+C', 'B+C'):
                    self.assertIn(pair, text)
                self.assertNotIn('requires B plus exactly one', text)

    def test_save_flow_does_not_route_through_a_done_action(self):
        text = (ROOT / 'auth/onboarding/id-parsing/flow.md').read_text()
        self.assertNotIn('-->|Done|', text)
        self.assertIn('automatically', text)
        self.assertIn('Review ID details', text)

    def test_camera_disclosure_keeps_recovery_and_standalone_boundary(self):
        text = (ROOT / 'auth/onboarding/id-capture/ui.md').read_text()
        for term in ('IdentityCameraAfterDisclosure', 'Settings', 'standalone', 'denial'):
            self.assertIn(term, text)

    def test_catalog_names_current_owners_and_immutable_evidence(self):
        data = json.loads((ROOT / 'docs/repositories.json').read_text())
        rows = {row['repository']: row for row in data['repositories']}
        for name in ('android.apexfission.auth', 'go.attestra.aws',
                     'go.apexfission.aws.auth', 'go.apexfission.aws.verifyemail',
                     'go.appexfission.aws.card-capture', 'go.infra.composer',
                     'android.ui.common'):
            with self.subTest(repository=name):
                row = rows['lambdawalker/' + name]
                self.assertRegex(row['source_ref'], r'^[0-9a-f]{40}$')
                self.assertTrue(row['agent_entry'].startswith('https://raw.githubusercontent.com/'))
        self.assertNotIn('lambdawalker/android.attestra.auth', rows)

    def test_reviewed_agent_translations_match_canonical_source(self):
        translations = json.loads((ROOT / 'sites/translations.json').read_text())
        for source, item in translations.items():
            with self.subTest(source=source):
                self.assertEqual(hashlib.sha256((ROOT / source).read_bytes()).hexdigest(),
                                 item['source_sha256'])
                self.assertTrue((ROOT / item['path']).is_file())

    def test_working_transfer_files_are_not_deliverables(self):
        self.assertFalse((ROOT / '.github/audit-transfer').exists())
        self.assertFalse(list((ROOT / '.github/workflows').glob('*temporary*')))


if __name__ == '__main__':
    unittest.main()
