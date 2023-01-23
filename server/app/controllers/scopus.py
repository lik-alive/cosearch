import os
import requests
from app.db import db
from app.models.paper import Paper
from app.actions.helper import compstr
from config import Config


class Scopus:
    """Scopus linker."""

    @staticmethod
    def link():
        # for paper in db.session.query(Paper).all():
        #     if not (paper.id >= 0 and paper.id <= 1000):
        #         continue

        #     # Skip already linked
        #     if paper.eid is not None:
        #         continue

        #     # Link by DOI
        #     if paper.doi is not None:
        #         Scopus.linkByField('DOI', paper.doi, paper)
        #     # else:
        #     #     Scopus.linkByField('TITLE', paper.title_en, paper)

        Scopus.processIssues()

        db.session.commit()
        db.session.close()
        return 'Success'

    """Search paper by field (DOI, TITLE, VOLUME, ISSUE)"""

    @staticmethod
    def linkByField(search_field, search_value, paper):
        data = Scopus.searchRequest(f"{search_field}({search_value})")

        if 'search-results' in data and data['search-results']['opensearch:totalResults'] == '1':
            entry = data['search-results']['entry'][0]
            if entry['prism:publicationName'] == 'Computer Optics':
                paper.eid = entry['eid']
                paper.citedcount = entry['citedby-count']

                if search_field == 'TITLE':
                    print(paper.issue, paper.no, entry['prism:volume'],
                          entry['prism:issueIdentifier'])
                else:
                    print(paper.issue, paper.no)

            else:
                print('!!!Wrong journall', paper.issue, paper.no,
                      data['search-results']['entry'][0]['prism:publicationName'])
        else:
            print(f'!!!Not found by {search_field}', paper.issue, paper.no)

        return

    """Find first difference in two strings"""

    @staticmethod
    def printStrdif(str1, str2):
        for i in range(0, min(len(str1), len(str2))):
            if str1[i] != str2[i]:
                print(i, str1[i], str2[i])
                break

        return

    """Search paper by field (DOI, TITLE, VOLUME, ISSUE)"""

    @staticmethod
    def linkByIssue(vol, no, papers):
        data = Scopus.searchRequest(
            f"SOURCE-ID(21100203110) and VOLUME({vol}) and ISSUE({no})")

        if 'search-results' in data and data['search-results']['opensearch:totalResults'] != '0':
            for entry in data['search-results']['entry']:
                found = False
                similar = 0
                similarData = []
                # Fix symbols
                scopusTitle = entry['dc:title']
                scopusTitle = scopusTitle.replace('’', "'")
                scopusTitle = scopusTitle.replace('‘', "'")
                scopusTitle = scopusTitle.replace('“', '"')
                scopusTitle = scopusTitle.replace('”', '"')
                scopusTitle = scopusTitle.replace('–', '-')
                # Fix final dot (it happens occasionally)
                scopusDoi = None
                if 'prism:doi' in entry:
                    scopusDoi = entry['prism:doi']
                    if scopusDoi[-1] == '.':
                        scopusDoi = scopusDoi[:-1]

                for paper in papers:
                    if paper.title_en is None:
                        continue

                    # Already found
                    if paper.eid == entry['eid']:
                        print(paper.issue, paper.no)

                        if paper.title_en.lower() != scopusTitle.lower():
                            print("!!!Already found but different in titles",
                                  paper.issue, paper.no)
                            print(paper.title_en)
                            print(scopusTitle)
                            Scopus.printStrdif(
                                paper.title_en.lower(), scopusTitle.lower())

                        if paper.doi != scopusDoi:
                            print('!!!Already found but different in DOI',
                                  paper.issue, paper.no)
                            print(paper.doi)
                            print(scopusDoi)
                            Scopus.printStrdif(
                                paper.doi, scopusDoi)

                        found = True
                        similar = False
                        break

                    # Search by equality
                    if paper.title_en.lower() == scopusTitle.lower():
                        paper.eid = entry['eid']
                        paper.citedcount = entry['citedby-count']

                        print(paper.issue, paper.no, 'assigned')

                        if paper.doi != scopusDoi:
                            print('!!!Different DOI', paper.issue, paper.no)
                            print(paper.doi)
                            print(scopusDoi)
                            Scopus.printStrdif(
                                paper.doi, scopusDoi)

                        found = True
                        similar = False
                        break
                    # Search by similarity
                    elif compstr(paper.title_en, scopusTitle) > 80:
                        found = True
                        if compstr(paper.title_en, scopusTitle) > similar:
                            similar = compstr(paper.title_en, scopusTitle)
                            similarData = [paper.issue, paper.no, entry['eid'],
                                           entry['citedby-count'], paper.title_en, scopusTitle]

                if similar > 0:
                    print('!!!Very similar titles',
                          similarData[0], similarData[1], similarData[2], similarData[3])
                    print(similarData[4])
                    print(similarData[5])

                if not found:
                    print('!!!Not found a paper to link',
                          f"{vol}-{no}", scopusTitle, entry['eid'], entry['citedby-count'])
        else:
            print('!!!Issue not found', f"{vol}-{no}")
            if 'service-error' in data:
                print('!!!Error',
                      data['service-error']['status']['statusText'])

        return

    """Search paper by DOI/Title"""

    @staticmethod
    def processIssues():
        items = db.session.query(Paper.issue).group_by(Paper.issue).all()

        for item in items:
            issue = item[0]

            vol = issue[0:issue.index(
                '-')] if '-' in issue else issue
            no = issue[issue.index('-')+1:] if '-' in issue else '0'

            # Skip non-scopus issues
            if int(vol) <= 31:
                continue

            # Skip already checked issues
            if not (int(vol) >= 34 and int(vol) <= 34):
                continue

            papers = db.session.query(Paper).filter(Paper.issue == issue).all()

            Scopus.linkByIssue(vol, no, papers)

        return

    """Search  request"""
    @staticmethod
    def searchRequest(query, start=0, popularFirst=False, post=False):
        if post:
            headers = {
                'Accept': 'application/json',
                'X-ELS-APIKey': Config.ELS_KEY
            }

            data = {
                'query': query,
                'start': start,
                'count': 25
            }
            if popularFirst:
                data['sort'] = 'citedby-count'

            r = requests.post(
                "https://api.elsevier.com/content/search/scopus", headers=headers, data=data)
        else:
            params = {
                'query': query,
                'start': start,
                'apiKey': Config.ELS_KEY
            }
            if popularFirst:
                params['sort'] = 'citedby-count'

            r = requests.get(
                "https://api.elsevier.com/content/search/scopus", params=params)

        data = r.json()

        return data

    """Data fixer"""
    @staticmethod
    def fix():
        # HOT FIXES
        paper = db.session.query(Paper).filter(
            Paper.issue == '47-1').filter(Paper.no == 8).first()
        paper.title_en = "Optimization, fabrication and characterization of a binary subwavelength cylindrical terahertz lens"

        paper = db.session.query(Paper).filter(
            Paper.issue == '46-2').filter(Paper.no == 9).first()
        paper.title_en = "Estimation of the cross-wind speed from turbulent fluctuations of the image of a diffuse target illuminated by a laser beam"

        paper = db.session.query(Paper).filter(
            Paper.issue == '46-2').filter(Paper.no == 1).first()
        paper.title_en = "Method for calculating the eikonal function and its application to design of diffractive optical elements for optical beam shaping"

        paper = db.session.query(Paper).filter(
            Paper.issue == '46-3').filter(Paper.no == 15).first()
        paper.title_en = "Novel Approach of Simplification Detected Contours on X-Ray Medical Images"

        paper = db.session.query(Paper).filter(
            Paper.issue == '46-4').filter(Paper.no == 10).first()
        paper.title_en = "Neural network application for semantic segmentation of fundus"

        paper = db.session.query(Paper).filter(
            Paper.issue == '46-4').filter(Paper.no == 8).first()
        paper.title_en = "Document image analysis and recognition: a survey"

        paper = db.session.query(Paper).filter(
            Paper.issue == '46-4').filter(Paper.no == 7).first()
        paper.title_en = "Genetic algorithm for optimizing Bragg and hybrid metal-dielectric reflectors"

        paper = db.session.query(Paper).filter(
            Paper.issue == '46-6').filter(Paper.no == 2).first()
        paper.title_en = "Topological charge of superposition of optical vortices described by a geometric sequence"

        paper = db.session.query(Paper).filter(
            Paper.issue == '46-6').filter(Paper.no == 10).first()
        paper.title_en = "Comparative analysis of reflection symmetry detection methods in binary raster images with skeletal and contour representations"

        paper = db.session.query(Paper).filter(
            Paper.issue == '45-1').filter(Paper.no == 17).first()
        paper.title_en = "Chest x-ray image classification for viral pneumonia and Сovid-19 using neural networks"

        paper = db.session.query(Paper).filter(
            Paper.issue == '45-1').filter(Paper.no == 16).first()
        paper.title_en = "Discrete orthogonal transforms on lattices of integer elements of quadratic fields"

        paper = db.session.query(Paper).filter(
            Paper.issue == '45-1').filter(Paper.no == 15).first()
        paper.title_en = "Deep learning-based video stream reconstruction in mass-production diffractive optical systems"

        paper = db.session.query(Paper).filter(
            Paper.issue == '45-1').filter(Paper.no == 8).first()
        paper.title_en = "Optical system calibration for 3D measurements in a hydrodynamic tunnel"

        paper = db.session.query(Paper).filter(
            Paper.issue == '45-2').filter(Paper.no == 13).first()
        paper.title_en = "Identification of pathological changes in the lungs using an analysis of radiological reports and tomographic images"

        paper = db.session.query(Paper).filter(
            Paper.issue == '45-2').filter(Paper.no == 15).first()
        paper.title_en = "A method for mobile device positioning using a sensor network of ble beacons, approximation of the rssi value and artificial neural networks"

        paper = db.session.query(Paper).filter(
            Paper.issue == '45-2').filter(Paper.no == 16).first()
        paper.title_en = "Development of a cognitive mnemonic scheme for an optical smart-technology of remote learning based of artificial immune systems"

        paper = db.session.query(Paper).filter(
            Paper.issue == '45-2').filter(Paper.no == 8).first()
        paper.title_en = "Tunable LiNbO3-based diffractive optical element for the control of transverse modes of a laser beam"

        paper = db.session.query(Paper).filter(
            Paper.issue == '45-3').filter(Paper.no == 9).first()
        paper.title_en = "Non-Markovian decoherence of a two-level system in a lorentzian bosonic reservoir and a stochastic environment with finite correlation time"

        paper = db.session.query(Paper).filter(
            Paper.issue == '45-3').filter(Paper.no == 18).first()
        paper.title_en = "Block algorithms to solve Zheng/Chen/Zhang’s finite-difference equations"

        paper = db.session.query(Paper).filter(
            Paper.issue == '45-4').filter(Paper.no == 3).first()
        paper.title_en = "Optical vortices with an infinite number of screw dislocations"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-2').filter(Paper.no == 7).first()
        paper.title_en = "An optical system for remote sensing in the UV, visible, and NIR spectral ranges"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-2').filter(Paper.no == 9).first()
        paper.eid = "2-s2.0-85083983711"
        paper.citedcount = 5

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-3').filter(Paper.no == 4).first()
        paper.title_en = "Transfer of spin angular momentum to a dielectric particle"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-3').filter(Paper.no == 18).first()
        paper.title_en = "Identification of the acoustic signal models of audio exchange systems under conditions of interference and acoustic feedback"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-3').filter(Paper.no == 6).first()
        paper.title_en = "Algorithm for reconstructing complex coefficients of laguerre–gaussian modes from the intensity distribution of their coherent superposition"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-3').filter(Paper.no == 13).first()
        paper.title_en = "The use of reference marks for precise tip positioning in scanning probe microscopy"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-3').filter(Paper.no == 17).first()
        paper.title_en = "Method for camera motion parameter estimation from a small number of corresponding points using quaternions"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-3').filter(Paper.no == 10).first()
        paper.title_en = "A method of contour detection based on an image weight model"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-3').filter(Paper.no == 20).first()
        paper.title_en = "Incremental learning of an abnormal behavior detection algorithm based on principal components"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-3').filter(Paper.no == 11).first()
        paper.title_en = "Quality control method of the transmission of fine image details in the JPEG2000"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-4').filter(Paper.no == 11).first()
        paper.title_en = "High-speed format 1000BASE-SX / LX transmission through the atmosphere by vortex beams near ir range with help modified SFP-transmers DEM-310GT"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-4').filter(Paper.no == 10).first()
        paper.doi = "10.18287/2412-6179-CO-702"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-4').filter(Paper.no == 17).first()
        paper.title_en = "Earth remote sensing imagery classification using a multi-sensor superresolution fusion algorithm"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-5').filter(Paper.no == 12).first()
        paper.title_en = "Searching and describing objects in satellite images on the basis of modeling reasoning"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-5').filter(Paper.no == 11).first()
        paper.title_en = "Remote sensing data retouching based on image inpainting algorithms in the forgery generation problem"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-5').filter(Paper.no == 21).first()
        paper.title_en = "Optimization of parameters of binary phase axicons for the generation of terahertz vortex surface plasmon polaritons on cylindrical conductors"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-5').filter(Paper.no == 7).first()
        paper.title_en = "Holographic memory updated by contradictory information: Influence of low frequency attenuation on response stability"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-5').filter(Paper.no == 18).first()
        paper.title_en = "An abstract model of an artificial immune network based on a classifier committee for biometric pattern recognition by the example of keystroke dynamics"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-5').filter(Paper.no == 2).first()
        paper.title_en = "High numerical aperture metalens to generate an energy backflow"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-5').filter(Paper.no == 10).first()
        paper.title_en = "Nonlinear filtering of image contours defined in a complex-valued code"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-5').filter(Paper.no == 9).first()
        paper.title_en = "Approaches to moving object detection and parameter estimation in a video sequence for the transport analysis system"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-6').filter(Paper.no == 3).first()
        paper.title_en = "The structure of normal modes in parallel ideal optical fibers with strong coupling"

        paper = db.session.query(Paper).filter(
            Paper.issue == '44-6').filter(Paper.no == 6).first()
        paper.title_en = "Spiral phase plate with multiple singularity centers"

        paper = db.session.query(Paper).filter(
            Paper.issue == '43-3').filter(Paper.no == 3).first()
        paper.title_en = "Measurement of the orbital angular momentum of an astigmatic Hermite-Gaussian beam"

        paper = db.session.query(Paper).filter(
            Paper.issue == '43-4').filter(Paper.no == 11).first()
        paper.title_en = "Estimation of resonance characteristics of single-layer surface-plasmon sensors in liquid solutions using Fano's approximation in the visible and infrared regions"

        paper = db.session.query(Paper).filter(
            Paper.issue == '43-4').filter(Paper.no == 8).first()
        paper.title_en = "Investigation of the topological charge stability for multi-ringed laguerre-gauss vortex beams to random distortions"

        paper = db.session.query(Paper).filter(
            Paper.issue == '43-4').filter(Paper.no == 7).first()
        paper.title_en = "Qubit dynamics in an external laser field"

        paper = db.session.query(Paper).filter(
            Paper.issue == '43-5').filter(Paper.no == 1).first()
        paper.title_en = "Formulation of the inverse problem of calculating the optical surface for an illuminating beam with a plane wavefront as the Monge-Kantorovich problem"

        paper = db.session.query(Paper).filter(
            Paper.issue == '43-6').filter(Paper.no == 6).first()
        paper.title_en = "The two reflector design problem for forming a flat wavefront from a point source as an optimal mass transfer problem"

        paper = db.session.query(Paper).filter(
            Paper.issue == '43-6').filter(Paper.no == 21).first()
        paper.title_en = "Investigation of the influence of amplitude spiral zone plate parameters on produced energy backflow"

        paper = db.session.query(Paper).filter(
            Paper.issue == '43-6').filter(Paper.no == 8).first()
        paper.title_en = "Optics-to-thz conversion of vortex beams using nonlinear difference frequency generation"

        paper = db.session.query(Paper).filter(
            Paper.issue == '43-6').filter(Paper.no == 9).first()
        paper.title_en = "Feasibility of generating surface plasmon polaritons with a given orbital momentum on cylindrical waveguides using diffractive optical elements"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-1').filter(Paper.no == 10).first()
        paper.title_en = 'Bauman MSTU scientific school "Zoom lens design": features of theory and practice'

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-2').filter(Paper.no == 19).first()
        paper.title_en = "Block algorithms of a simultaneous difference solution of d'Alembert's and Maxwell's equations"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-2').filter(Paper.no == 17).first()
        paper.title_en = "Comparative image filtering using monotonic morphological operators"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-2').filter(Paper.no == 12).first()
        paper.title_en = "Noise minimized high resolution digital holographic microscopy applied to surface topography"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-3').filter(Paper.no == 19).first()
        paper.title_en = "Morphological conditional estimates of image complexity and information content"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-3').filter(Paper.no == 1).first()
        paper.title_en = "A non-coherent holographic correlator based on a digital a micromirror device"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-3').filter(Paper.no == 10).first()
        paper.title_en = "Spatial spectrum of coherence signal for a defocused object image in digital holographic microscopy with partially spatially coherent illumination"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-4').filter(Paper.no == 8).first()
        paper.title_en = "Calculation of the angular momentum of an electromagnetic field inside a waveguide with absolutely conducting walls"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-4').filter(Paper.no == 11).first()
        paper.title_en = "Focusing of light beams with the phase apodization of the optical system"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-4').filter(Paper.no == 7).first()
        paper.title_en = "The connection between the phase problem in optics, focusing of radiation, and the Monge-Kantorovich problem"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-4').filter(Paper.no == 13).first()
        paper.doi = "10.18287/2412-6159-2018-42-4-637-656"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-5').filter(Paper.no == 1).first()
        paper.title_en = "A variety of Fourier-invariant Gaussian beams"
        paper.authors_en = "Kotlyar V.V., Kovalev A.A., Porfirev A.P."

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-5').filter(Paper.no == 3).first()
        paper.title_en = "Energy backflow in the focal spot of a cylindrical vector beam"
        paper.authors_en = "Stafeev S.S., Nalimov A.G., Kotlyar V.V."

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-5').filter(Paper.no == 14).first()
        paper.title_en = "Metric of fine structures distortion of compressed images"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-5').filter(Paper.no == 18).first()
        paper.title_en = "Earth remote sensing data processing technology for obtaining vegetation types maps"

        paper = db.session.query(Paper).filter(
            Paper.issue == '42-5').filter(Paper.no == 8).first()
        paper.title_en = "Investigation of photoinduced formation of microstructures on the surface of a carbaseole-containing azopolymer depending on the power density of incident beams"

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-1').filter(Paper.no == 4).first()
        paper.eid = "2-s2.0-85014887634"
        paper.citedcount = 35

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-1').filter(Paper.no == 4).first()
        paper.title_en = "Wave front aberration compensation of space telescopes with telescope temperature field adjustment"

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-2').filter(Paper.no == 6).first()
        paper.title_en = 'Spectral properties of nonlinear surface polaritons of mid-IR range in a "semiconductor-layered metamaterial" structure'

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-2').filter(Paper.no == 10).first()
        paper.doi = "10.18287/0134-2452-2017-41-2-218-226"

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-2').filter(Paper.no == 17).first()
        paper.doi = "10.18287/0134-2452-2017-41-2-284-290"

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-3').filter(Paper.no == 5).first()
        paper.title_en = 'Analysis of focusing light by a harmonic diffractive lens with regard for the refractiive index dispersion'

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-3').filter(Paper.no == 8).first()
        paper.title_en = 'Spatially inhomogeneous pattern formation due to parametric modulation in broad-area lasers'

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-4').filter(Paper.no == 14).first()
        paper.eid = "2-s2.0-85043346403"
        paper.citedcount = 10

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-4').filter(Paper.no == 14).first()
        paper.title_en = 'Conforming identification of the fundamental matrix in the image matching problem'

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-4').filter(Paper.no == 1).first()
        paper.title_en = 'Optical properties of lowest-energy carbon allotropes from first-principles calculations'

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-4').filter(Paper.no == 20).first()
        paper.eid = "2-s2.0-85043304894"
        paper.citedcount = 7

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-4').filter(Paper.no == 20).first()
        paper.title_en = 'Parallel implementation of a multi-view image segmentation algorithm using the hough transform'

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-5').filter(Paper.no == 1).first()
        paper.title_en = 'Modeling of surface plasmon resonance in a bent single-mode metallized optical fiber with a finite element method'

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-5').filter(Paper.no == 10).first()
        paper.title_en = 'Investigation of the electromagnetic field in one-dimensional photonic crystals with defects'

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-5').filter(Paper.no == 7).first()
        paper.title_en = 'Modeling a high numerical aperture micrometalens simulation with and a varying number of sectors'

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-5').filter(Paper.no == 11).first()
        paper.title_en = 'Peculiarites of the Doppler effect in a multimode waveguide'

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-5').filter(Paper.no == 21).first()
        paper.title_en = 'International Conference and Youth School «Information Technologies and Nanotechnology » (ITNT-2017)'

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-5').filter(Paper.no == 9).first()
        paper.title_en = 'Measurement of the optical thickness of a layered object from interfernece colors in white-light microscopy'

        paper = db.session.query(Paper).filter(
            Paper.issue == '41-6').filter(Paper.no == 6).first()
        paper.title_en = 'Holographic diffusers with controlled scattering indicatrix'

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-1').filter(Paper.no == 10).first()
        paper.eid = "2-s2.0-84961253495"
        paper.citedcount = 5
        paper.title_en = "Modeling the 'Smartlink connection' performance"
        paper.doi = "10.18287/2412-6179-2016-40-1-64-72"

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-1').filter(Paper.no == 9).first()
        paper.title_en = "Design of an optical divider for 'Smartlink connection' with use of SLA and FDM 3D printing technology"

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-2').filter(Paper.no == 7).first()
        paper.doi = "10.18287/2412-6179-2016-40-2-173-178"

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-3').filter(Paper.no == 8).first()
        paper.title_en = "Method for uncertainty evaluation of the spatial mating of high-precision optical and mechanical parts"

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-3').filter(Paper.no == 11).first()
        paper.doi = "10.18287/2412-6179-2016-40-3-388-394"

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-3').filter(Paper.no == 15).first()
        paper.doi = "10.18287/2412-6179-2016-40-3-416-421"

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-4').filter(Paper.no == 17).first()
        paper.title_en = "Extraction of knowledge and relevant linguistic means with efficiency estimation for the formation of subject-oriented text sets"

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-5').filter(Paper.no == 20).first()
        paper.eid = "2-s2.0-85001055664"
        paper.citedcount = 0

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-5').filter(Paper.no == 14).first()
        paper.title_en = "Development of an algorithm for automatic construction of a computational procedure of local image processing, based on the hierarchical regression"

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-5').filter(Paper.no == 18).first()
        paper.title_en = "Automatic target recognition algorithm for low-count terahertz images"

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-6').filter(Paper.no == 2).first()
        paper.title_en = "Defocus and numerical focusing in interference microscopy with wide temporal spectrum of illumination field"

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-6').filter(Paper.no == 19).first()
        paper.doi = "10.18287/2412-6179-2016-40-6-911-918"

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-6').filter(Paper.no == 9).first()
        paper.title_en = "Determination of organic contaminants concentration on the silica surface by lateral force microscopy"

        paper = db.session.query(Paper).filter(
            Paper.issue == '40-6').filter(Paper.no == 24).first()
        paper.title_en = "Reducing background false positives for face detection in surveillance feeds"

        # Typo
        paper = db.session.query(Paper).filter(
            Paper.issue == '40-6').filter(Paper.no == 16).first()
        paper.title_en = "Analysis of conditions that influence the properties of the consructed 3D-image features"

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-2').filter(Paper.no == 5).first()
        paper.title_en = "Research of Orbital Angular Momentum of Superpositions of Diffraction-Free Bessel Beams with a Complex Shift"

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-2').filter(Paper.no == 4).first()
        paper.title_en = "Calculation of the Resonant Radius of a Dielectric Cylinder Under Illumination by a Plane Te-Wave"

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-2').filter(Paper.no == 3).first()
        paper.title_en = "Using Coupled Photonic Crystal Cavities for Increasing of Sensor Sensitivity"

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-3').filter(Paper.no == 12).first()
        paper.title_en = 'Analysis of optical characteristics of various designs of a classical "Guest - Host" lc modulator'

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-3').filter(Paper.no == 19).first()
        paper.doi = '10.18287/0134-2452-2015-39-3-429-435'

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-3').filter(Paper.no == 4).first()
        paper.title_en = 'Simulation of the resonance focusing of picosecond and femtosecond pulses by use of a dielectric microcylinder'

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-3').filter(Paper.no == 3).first()
        paper.doi = '10.18287/0134-2452-2015-39-3-311-318'

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-3').filter(Paper.no == 5).first()
        paper.doi = '10.18287/0134-2452-2015-39-3-324-321'

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-3').filter(Paper.no == 10).first()
        paper.eid = "2-s2.0-84938060973"
        paper.citedcount = 16
        paper.title_en = 'Comparative study of the spectral characteristics of aspheric lenses'
        paper.doi = '10.18287/0134-2452-2015-39-3-363-239'

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-4').filter(Paper.no == 3).first()
        paper.eid = "2-s2.0-84945199246"
        paper.citedcount = 4
        paper.title_en = 'Angular momentum of a light field as superposition of hermite-gaussian modes'
        paper.doi = "10.18287/0134-2452-2015-39-4-459-461"

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-4').filter(Paper.no == 5).first()
        paper.title_en = 'A differential method for calculating X-ray diffraction by crystals: The scalar theory'

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-5').filter(Paper.no == 15).first()
        paper.title_en = "Study of informative feature selection approaches for the texture image recognition problem using Laws' masks"

        paper = db.session.query(Paper).filter(
            Paper.issue == '39-5').filter(Paper.no == 12).first()
        paper.title_en = "Investigation of temperature-induced lasing dynamics in broad-area VCSESL"

        paper = db.session.query(Paper).filter(
            Paper.issue == '38-1').filter(Paper.no == 9).first()
        paper.doi = '10.18287/0134-2452-2014-38-1-57-64'

        paper = db.session.query(Paper).filter(
            Paper.issue == '38-1').filter(Paper.no == 4).first()
        paper.title_en = "Solution of expanded pulse - propagation equation for optical fibers"

        paper = db.session.query(Paper).filter(
            Paper.issue == '38-1').filter(Paper.no == 3).first()
        paper.title_en = "Joint finite - difference solution of the d'Alembert and Maxwell’s equations. Two – dimensional case"

        paper = db.session.query(Paper).filter(
            Paper.issue == '38-2').filter(Paper.no == 11).first()
        paper.title_en = "Reflected four-zones subwavelength microoptics element for polarization conversion from linear to radial"

        paper = db.session.query(Paper).filter(
            Paper.issue == '38-2').filter(Paper.no == 7).first()
        paper.title_en = "Solution in quadratures of expanded pulse - propagation equation for optical fibers for an arbitrary nonlinearity"

        paper = db.session.query(Paper).filter(
            Paper.issue == '38-3').filter(Paper.no == 23).first()
        paper.title_en = "Recognition of zero bits of 3-sat problem by applying linear algebra's methods"

        paper = db.session.query(Paper).filter(
            Paper.issue == '38-3').filter(Paper.no == 2).first()
        paper.title_en = "Integration in elementary funktions of two-way pulse - propagation equation in optical fibers for power nonlinearity"

        paper = db.session.query(Paper).filter(
            Paper.issue == '38-4').filter(Paper.no == 42).first()
        paper.title_en = "Industrial datamatrix barcode recognition for an arbitrary camera angle and rotation"

        paper = db.session.query(Paper).filter(
            Paper.issue == '38-4').filter(Paper.no == 16).first()
        paper.title_en = "The solution of an expanded pulse - propagation equation in optical fibers for competing nonlinearity"

        paper = db.session.query(Paper).filter(
            Paper.issue == '38-4').filter(Paper.no == 40).first()
        paper.title_en = "Formation of features for improving the quality of medical diagnosis based on discriminant analysis methods"

        # Typo
        paper = db.session.query(Paper).filter(
            Paper.issue == '37-1').filter(Paper.no == 10).first()
        paper.title_en = "Complex vortex beams for of rotation of micromechanical elements"

        paper = db.session.query(Paper).filter(
            Paper.issue == '37-2').filter(Paper.no == 6).first()
        paper.title_en = "Orbital angular momentum of superposition of two generalized Hermite-Gaussian laser beams"

        paper = db.session.query(Paper).filter(
            Paper.issue == '37-3').filter(Paper.no == 3).first()
        paper.title_en = "Solution of pulse - propagation equation for optical fiber in quadratures"

        paper = db.session.query(Paper).filter(
            Paper.issue == '37-4').filter(Paper.no == 5).first()
        paper.title_en = "The modification of laser beam for optimization of optical trap force characteristics"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-1').filter(Paper.no == 12).first()
        paper.eid = "2-s2.0-84926241403"
        paper.citedcount = 3
        paper.title_en = "Experimental realisation of microparticle's optical trapping by use of binary radial DOE"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-1').filter(Paper.no == 17).first()
        paper.eid = "2-s2.0-84926240755"
        paper.citedcount = 5
        paper.title_en = "Object detection and recognition in the driver assistance system based on the fractal analysis"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-1').filter(Paper.no == 3).first()
        paper.eid = "2-s2.0-84926235049"
        paper.citedcount = 8
        paper.title_en = "The perturbation theory for Schrodinger equation in the periodic environment in momentum representation"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-1').filter(Paper.no == 18).first()
        paper.eid = "2-s2.0-84922686119"
        paper.citedcount = 10

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-2').filter(Paper.no == 6).first()
        paper.eid = "2-s2.0-84926242331"
        paper.citedcount = 5
        paper.title_en = "Focusing of linearly polarized light using binary axicon with subwavelength period"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-2').filter(Paper.no == 9).first()
        paper.eid = "2-s2.0-84926235327"
        paper.citedcount = 3

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-2').filter(Paper.no == 13).first()
        paper.eid = "2-s2.0-84924732166"
        paper.citedcount = 3

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-2').filter(Paper.no == 17).first()
        paper.eid = "2-s2.0-84924661846"
        paper.citedcount = 4
        paper.title_en = "Determination of coordinates and parameters of movement of object on the basis of processing of images"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-2').filter(Paper.no == 16).first()
        paper.eid = "2-s2.0-84922686410"
        paper.citedcount = 9
        paper.title_en = "An algorithm for automatic construction of computational procedure of non-linear local image processing on the base of hierarchical regression"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-2').filter(Paper.no == 4).first()
        paper.eid = "2-s2.0-84922686263"
        paper.citedcount = 2
        paper.title_en = "Higher-order polarization mode dispersion mathematical models for silica anisotropic optical waveguide"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-2').filter(Paper.no == 5).first()
        paper.eid = "2-s2.0-84922686144"
        paper.citedcount = 6
        paper.title_en = "Analogue of Rayleigh-Sommerfeld integral for anisotropic and gyrotropic media"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-2').filter(Paper.no == 18).first()
        paper.title_en = "Discretization of continuous contours of images, defined in a complex-valued form"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-2').filter(Paper.no == 11).first()
        paper.eid = "2-s2.0-84922685332"
        paper.citedcount = 9
        paper.title_en = "Reducing of the focal spot size at radial polarization by means of the binary annular element"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-3').filter(Paper.no == 13).first()
        paper.eid = "2-s2.0-84922685692"
        paper.citedcount = 9
        paper.title_en = "Modeling and investigation superachromatozation refractive and refractive-diffractive optical systems"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-4').filter(Paper.no == 8).first()
        paper.eid = "2-s2.0-84926233490"
        paper.citedcount = 7
        paper.title_en = "Joint solution of the Klein-Gordon And Maxwell's equations"

        paper = db.session.query(Paper).filter(
            Paper.issue == '36-4').filter(Paper.no == 9).first()
        paper.eid = "2-s2.0-84922687394"
        paper.citedcount = 3
        paper.title_en = "Joint finite-difference solution of the dalamber and Maxwell's equations. One-dimensional case"

        paper = db.session.query(Paper).filter(
            Paper.issue == '35-1').filter(Paper.title_ru.like("%подготовки рукописей%")).first()
        paper.eid = "2-s2.0-85081418088"
        paper.citedcount = 0
        paper.title_en = "Guidelines for authors of the journal of Computer Optics"

        paper = db.session.query(Paper).filter(
            Paper.issue == '35-1').filter(Paper.no == 7).first()
        paper.eid = "2-s2.0-84875691533"
        paper.citedcount = 1
        paper.title_en = "Metal-dielectric Mikaelan's lense"

        paper = db.session.query(Paper).filter(
            Paper.issue == '35-1').filter(Paper.no == 10).first()
        paper.eid = "2-s2.0-84861866482"
        paper.citedcount = 9
        paper.title_en = 'Optimization of binary doe for formation of the "light bottle"'

        paper = db.session.query(Paper).filter(
            Paper.issue == '35-2').filter(Paper.no == 6).first()
        paper.eid = "2-s2.0-84871777613"
        paper.citedcount = 17
        paper.title_en = "The research of intensification's expedients for nanoporous structures formation in metal materials by the selective laser sublimation of alloy's components"

        paper = db.session.query(Paper).filter(
            Paper.issue == '34-1').filter(Paper.title_ru.like("%подготовки рукописей%")).first()
        paper.eid = "2-s2.0-85081414051"
        paper.citedcount = 0
        paper.title_en = "Guidelines for authors of the journal of Computer Optics"

        paper = db.session.query(Paper).filter(
            Paper.issue == '34-1').filter(Paper.no == 6).first()
        paper.eid = "2-s2.0-84855218256"
        paper.citedcount = 3
        paper.title_en = "Speckle-photography and holographic interferometry with digital recording of diffraction field in Fourier plane"

        paper = db.session.query(Paper).filter(
            Paper.issue == '34-1').filter(Paper.no == 2).first()
        paper.eid = None
        # paper.citedcount = 17
        paper.title_en = "Light spot diameter in the near zone of binary diffractive microaxicon"

        paper = db.session.query(Paper).filter(
            Paper.issue == '34-2').filter(Paper.title_ru.like("%подготовки рукописей%")).first()
        paper.eid = "2-s2.0-85081418121"
        paper.citedcount = 0
        paper.title_en = "Guidelines for authors of the journal of Computer Optics"

        paper = db.session.query(Paper).filter(
            Paper.issue == '34-3').filter(Paper.title_ru.like("%подготовки рукописей%")).first()
        paper.eid = "2-s2.0-85081418211"
        paper.citedcount = 0
        paper.title_en = "Guidelines for authors of the journal of Computer Optics"

        paper = db.session.query(Paper).filter(
            Paper.issue == '34-3').filter(Paper.no == 16).first()
        paper.eid = "2-s2.0-84863435039"
        paper.citedcount = 3
        paper.title_en = "Linear filtering of continuous contours of images, defined in a complex form"

        paper = db.session.query(Paper).filter(
            Paper.issue == '34-4').filter(Paper.title_ru.like("%подготовки рукописей%")).first()
        paper.eid = "2-s2.0-85081418884"
        paper.citedcount = 0
        paper.title_en = "Guidelines for authors of the journal of Computer Optics"

        paper = db.session.query(Paper).filter(
            Paper.issue == '34-4').filter(Paper.no == 12).first()
        paper.eid = "2-s2.0-84945972679"
        paper.citedcount = 4

        paper = db.session.query(Paper).filter(
            Paper.issue == '34-4').filter(Paper.no == 1).first()
        paper.eid = "2-s2.0-84926235022"
        paper.citedcount = 3

        paper = db.session.query(Paper).filter(
            Paper.issue == '34-4').filter(Paper.no == 19).first()
        paper.eid = "2-s2.0-84907423146"
        paper.citedcount = 2
        paper.title_en = "Gaussian integers representation in Pitti's number system"

        paper = db.session.query(Paper).filter(
            Paper.issue == '33-2').filter(Paper.title_ru.like("%подготовки рукописей%")).first()
        paper.eid = "2-s2.0-85081420340"
        paper.citedcount = 0
        paper.title_en = "Guidelines for authors of the journal of Computer Optics"

        paper = db.session.query(Paper).filter(
            Paper.issue == '33-3').filter(Paper.title_ru.like("%подготовки рукописей%")).first()
        paper.eid = "2-s2.0-85081418761"
        paper.citedcount = 0
        paper.title_en = "Guidelines for authors of the journal of Computer Optics"

        paper = db.session.query(Paper).filter(
            Paper.issue == '33-3').filter(Paper.no == 5).first()
        paper.eid = "2-s2.0-84945944744"
        paper.citedcount = 0
        paper.title_en = "D.Gabor's scheme optimization for computer hologram recording"

        paper = db.session.query(Paper).filter(
            Paper.issue == '33-4').filter(Paper.title_ru.like("%подготовки рукописей%")).first()
        paper.eid = "2-s2.0-85081417417"
        paper.citedcount = 0
        paper.title_en = "Guidelines for authors of the journal of Computer Optics"

        paper = db.session.query(Paper).filter(
            Paper.issue == '32-1').filter(Paper.no == 10).first()
        paper.eid = "2-s2.0-85030866629"
        paper.citedcount = 0

        paper = db.session.query(Paper).filter(
            Paper.issue == '32-1').filter(Paper.no == 2).first()
        paper.eid = "2-s2.0-85030834390"
        paper.citedcount = 0
        paper.title_en = "I.N. Sisakyan's scientific works on diffractive and fiber optics"

        paper = db.session.query(Paper).filter(
            Paper.issue == '32-2').filter(Paper.no == 4).first()
        paper.eid = "2-s2.0-85019187031"
        paper.citedcount = 6
        paper.title_en = "Integral representations of solutions of Maxwell's equations in the form of the spectrum of surface electromagnetic waves"

        paper = db.session.query(Paper).filter(
            Paper.issue == '32-2').filter(Paper.no == 3).first()
        paper.eid = "2-s2.0-84945936442"
        paper.citedcount = 2
        paper.title_en = "Design and analysis of diffractive micro- and nano-structures"

        paper = db.session.query(Paper).filter(
            Paper.issue == '32-2').filter(Paper.no == 12).first()
        paper.eid = "2-s2.0-77952592639"
        paper.citedcount = 18
        paper.title_en = "Design of radially-symmetrical refractive surface taking into account Fresnel loss"

        paper = db.session.query(Paper).filter(
            Paper.issue == '32-3').filter(Paper.no == 11).first()
        paper.eid = "2-s2.0-85021717322"
        paper.citedcount = 3

        paper = db.session.query(Paper).filter(
            Paper.issue == '32-3').filter(Paper.no == 16).first()
        paper.eid = "2-s2.0-85031038591"
        paper.citedcount = 2

        paper = db.session.query(Paper).filter(
            Paper.issue == '32-4').filter(Paper.no == 6).first()
        paper.eid = "2-s2.0-84989934382"
        paper.citedcount = 6

        paper = db.session.query(Paper).filter(
            Paper.issue == '32-4').filter(Paper.no == 3).first()
        paper.eid = "2-s2.0-84945940978"
        paper.citedcount = 2

        paper = db.session.query(Paper).filter(
            Paper.issue == '32-4').filter(Paper.no == 5).first()
        paper.eid = "2-s2.0-84926236830"
        paper.citedcount = 4

        paper = db.session.query(Paper).filter(
            Paper.issue == '32-4').filter(Paper.no == 12).first()
        paper.eid = "2-s2.0-84926232915"
        paper.citedcount = 3

        paper = db.session.query(Paper).filter(
            Paper.issue == '32-4').filter(Paper.no == 10).first()
        paper.eid = "2-s2.0-84871953787"
        paper.citedcount = 2

        """ SCOPUS ERRORS
cosearch-server | !!!Already found but different in titles 46-2 18
cosearch-server | Transformer point net: cost-efficient classification of on-road objects captured by light ranging sensors on low-resolution conditions
cosearch-server | NUMERICAL METHODS AND DATA ANALYSIS Transformer point net: cost-efficient classification of on-road objects captured by light ranging sensors on low-resolution conditions

cosearch-server | !!!Different DOI 45-3 8
cosearch-server | 10.18287/2412-6179-CO-788
cosearch-server | 10.18287/2412-6179-788

cosearch-server | !!!Already found but different in titles 45-3 12
cosearch-server | Multispectral optoelectronic device for controlling an autonomous mobile platform
cosearch-server | Image processing, pattern recognition: Multispectral optoelectronic device for controlling an autonomous mobile platform

cosearch-server | !!!Already found but different in titles 45-5 2
cosearch-server | Optical phase singularities and superluminal motion in unbounded space
cosearch-server | Optical phase singularities going to and coming from infinity with a higher-than-light speed

cosearch-server | !!!Already found but different in titles 45-6 10
cosearch-server | Retinal biometric identification using convolutional neural network
cosearch-server | Image processing, pattern recognition retinal biometric identification using convolutional neural network

cosearch-server | !!!Already found but different in titles 44-3 7
cosearch-server | An efficient algorithm for overlapping bubbles segmentation
cosearch-server | Image processing, pattern recognition an efficient algorithm for overlapping bubbles segmentation

cosearch-server | !!!Already found but different in titles 44-4 12
cosearch-server | Cross-layer optimization technology for wireless network multimedia video
cosearch-server | Image processing, pattern recognition cross-layer optimization technology for wireless network multimedia video

cosearch-server | !!!Already found but different in titles 44-4 5
cosearch-server | Necessary conditions for the propagation of two modes, LP01 and LP11, in a step-index optical fiber with a Kerr nonlinearity
cosearch-server | Necessary conditions for the propagation of two modes, lp<inf>01</inf> and lp<inf>11</inf>, in a step-index optical fiber with a kerr nonlinearity

cosearch-server | !!!Very similar titles 44-2 9 2-s2.0-85083983711 5
cosearch-server | Designing multilayer dielectric filter based on TiO2/SiO2 for fluorescence microscopy applications
cosearch-server | Designing multilayer dielectric filter based on TiO<inf>2</inf>/SiO<inf>2</inf> for fluorescence microscopy applications

cosearch-server | !!!Already found but different in titles 43-1 16
cosearch-server | Gradation trajectories as an analog of gradation curves in the metric CIE Lab space: discrete approach
cosearch-server | Gradation trajectories as an analog of gradation curves in the metric cie lab space: Discretes approach

cosearch-server | !!!Different DOI 43-5 4
cosearch-server | 10.18287/2412-6179-2019-43-5-735-740
cosearch-server | 10.18287/2412-6179-2019-43-5-734-740

cosearch-server | !!!Already found but different in titles 42-2 20
cosearch-server | Algorithm for eliminating gas absorption effects on hyperspectral remote sensing data
cosearch-server | Algorithm for eliminating gas absorption effects on hypertispectral remote sensing data

cosearch-server | !!!Different DOI 42-4 9
cosearch-server | 10.18287/2412-6179-2018-42-4-606-613
cosearch-server | 10.18287/2412-6179-2017-42-4-606-613

cosearch-server | !!!Already found but different in titles 41-4 9
cosearch-server | An efficient block-based algorithm for hair removal in dermoscopic images
cosearch-server | Image processing, pattern recognition: An efficient block-based algorithm for hair removal in dermoscopic images

cosearch-server | !!!Already found but different in DOI 41-1 4
cosearch-server | 10.18287/0134-2452-2017-41-1-30-36
cosearch-server | 10.18287/2412-6179-2017-41-1-30-36

cosearch-server | !!!Already found but different in DOI 41-4 14
cosearch-server | 10.18287/2412-6179-2017-41-559-563
cosearch-server | 10.18287/2412-6179-2017-41-4-559-563

cosearch-server | !!!Already found but different in DOI 41-4 20
cosearch-server | 10.18287/2412-6179-2017-41-588-591
cosearch-server | 10.18287/2412-6179-2017-41-4-588-591

nbsp here! (57 index)
cosearch-server | !!!Already found but different in titles 41-1 13
cosearch-server | Classification algorithm of parking space images based on a histogram of oriented gradients and support vector machines
cosearch-server | Classification algorithm of parking space images based on a histogram of oriented gradients and support vector machines

cosearch-server | !!!Already found but different in titles 40-4 15
cosearch-server | A method for optoelectronic control of liquid volume in a tank
cosearch-server | Method for optoelectronic control of liquid volume in a tank

cosearch-server | !!!Already found but different in titles 39-1 2
cosearch-server | Analysis of interference of radially polarized laser beams generated by ring optical elements with a vortex phase at sharp focusing
cosearch-server | Analysis of interference of cylindrical laser beams generated by ring optical elements with a vortex phase at sharp focusing

cosearch-server | !!!Already found but different in titles 39-3 14
cosearch-server | Determination of conditions for the laser-induced intensification of mass transfer processes in the solid phase of metallic materials
cosearch-server | Determination of conditions for the laser-induced intensification of of mass transfer processes in the solid phase of metallic materials

cosearch-server | !!!Different DOI 39-5 18
cosearch-server | 10.18287/0134-2452-2015-39-5-770-775
cosearch-server | 10.18287/0134-2452-2015-39-5-770-776

cosearch-server | !!!Different DOI 39-5 6
cosearch-server | 10.18287/0134-2452-2015-39-5-678-687
cosearch-server | 10.18287/0134-2452-2015-39-5-678-686

cosearch-server | !!!Already found but different in titles 37-3 2
cosearch-server | Modulation instability of packets in inhomogeneous light guides
cosearch-server | Guidelines for authors of the journal of computer optics

cosearch-server | !!!Already found but different in titles 36-1 3
cosearch-server | The perturbation theory for Schrodinger equation in the periodic environment in momentum representation
cosearch-server | The theory of indignations for Schrodinger equation in the periodic environment in momentum representation representation

cosearch-server | !!!Already found but different in titles 36-1 18
cosearch-server | Conformed identification in corresponding points detection problem
cosearch-server | Identification in corresponding points detection problem

cosearch-server | !!!Already found but different in titles 32-2 4
cosearch-server | Integral representations of solutions of Maxwell's equations in the form of the spectrum of surface electromagnetic waves
cosearch-server | Solution of Maxwell's equations in the integral form of a spectrum of surface plasmons

osearch-server | !!!Already found but different in titles 32-2 2
cosearch-server | Nanophotonics - the manipulation of light by nanostructures
cosearch-server | Nanophotonics: Light manipulation using nanostructures

cosearch-server | !!!Already found but different in titles 32-2 12
cosearch-server | Design of radially-symmetrical refractive surface taking into account Fresnel loss
cosearch-server | Design of radiosymmetrical refractive surfaces with taking Fresnel loss into account

cosearch-server | !!!Already found but different in titles 32-3 16
cosearch-server | Face recognition on the basis of conjugation indexes in the space of summarizing invariants
cosearch-server | Feature space reduction using multicollinearity features

cosearch-server | !!!Already found but different in titles 32-3 11
cosearch-server | Method of rapid correlation using ternary templates for object recognition in images
cosearch-server | The method of fast correlation using ternary templates for object recognition on images

cosearch-server | !!!Already found but different in titles 32-4 9
cosearch-server | Approximate method of optical energy distribution calculation in multiple scattering media
cosearch-server | Approximate method of optical energy distribution calculation in multiple scattering mediums

cosearch-server | !!!Already found but different in titles 32-4 6
cosearch-server | Fabrication of three-dimensional photonics crystals by interference lithography with low light absorption
cosearch-server | Synthesis of three-dimensional photonic crystals by interference lithography with low light absorbtion

cosearch-server | !!!Already found but different in titles 32-4 3
cosearch-server | Geometric-optics design of focusators into a line in noparaxial case
cosearch-server | The design of the diffractive optical element to focus into a line in noparaxial case

cosearch-server | !!!Already found but different in titles 32-4 5
cosearch-server | Laser nanostructurizing of metal materials by application of moveable radiation focusators
cosearch-server | Laser nanostructurizing of metal materials by application of moveable radiation

osearch-server | !!!Already found but different in titles 32-4 12
cosearch-server | Face recognition on the basis of conjugation indexes in the space of summarizing invariants
cosearch-server | Face recognition using conjugation indices in the summation invariants

cosearch-server | !!!Already found but different in titles 32-4 10
cosearch-server | The semiconductor light is the light source, an alternative to incandescent lamps, and electroluminescent lamps
cosearch-server | The semiconducror lamp - as a source of illumination - an analog of vacuum and electroluminescent


        """

        db.session.commit()
        db.session.close()

        return 'Success'

    """Test EID"""
    @staticmethod
    def eidTest():
        papers = db.session.query(Paper).filter(Paper.eid != None).all()

        query = ""
        count = 0
        i = 0
        while i < len(papers):
            paper = papers[i]
            i += 1

            if count == 0:
                query = f"EID({paper.eid})"
                count += 1
            else:
                query += f" or EID({paper.eid})"
                count += 1

            print(i, count)

            if count == 25 or i == len(papers):
                data = Scopus.searchRequest(query)

                if 'search-results' in data and data['search-results']['opensearch:totalResults'] == str(count):
                    print("OK")

                else:
                    print('!!!Something happened')
                    print(query)
                    print(data['search-results']
                          ['opensearch:totalResults'], count)
                    if 'service-error' in data:
                        print('!!!Error',
                              data['service-error']['status']['statusText'])

                query = ""
                count = 0

        return "Success"
