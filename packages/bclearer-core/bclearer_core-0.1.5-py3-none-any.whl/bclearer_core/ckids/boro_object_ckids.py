from enum import Enum


class BoroObjectCkIds(Enum):
    NotSet = 0

    # region Top Ontology

    Objects = 1
    Types = 2
    Elements = 3
    Tuples = 4
    PlaceableObjects = 5
    PlaceableTypes = 6
    NonPlaceableTypes = 7
    TypesInstances = 8
    SuperSubTypes = 9
    WholesParts = 10
    TypePlaces = 11

    # endregion  // Top Ontology

    # region Ontology

    AcyclicCoupleTypes = 1001
    AntisymmetricCoupleTypes = 1002
    AsymmetricCoupleTypes = 1003
    CharacterStrings = 1004
    Couples = 1005
    CycleTupleTypes = 1006
    CyclicTupleTypes = 1007

    DescribedBy = 1008
    DescribingSpaces = 1009
    Descriptions = 1010
    FixedArityTupleTypes = 1011
    HomogenousFiniteCountTypeTypes = (
        1012
    )
    IntendedCharacterEquivalentStringNames = (
        1013
    )
    IntendedDistinctCharactersNamingSpaces = (
        1014
    )
    IntendedReservedCharactersNamingSpaces = (
        1015
    )
    IntendedUniqueCharactersNamingSpaces = (
        1016
    )
    IntransitiveCoupleTypes = 1017
    IrreflexiveCouples = 1018
    IrreflexiveCoupleTypes = 1019
    NamedBy = 1020
    Names = 1021
    NamesPowertype = 1022
    NamingSpaces = 1023
    NfAlternateNames = 1024
    NfBusinessDomainDescriptions = 1025
    NfCommonReservedNames = 1026
    NfEarCommonReservedNames = 1027
    NonWellFoundedTypesInstances = 1028
    NumberOfFiniteCountTypesInstancesTypes = (
        1029
    )
    PartialOrderCoupleTypes = 1030
    PowerTypesInstances = 1031
    ProximalSuperSubTypes = 1032
    ProximalTypesInstances = 1033
    ProximalWholesParts = 1034
    Quadruples = 1035
    ReflexiveCouples = 1036
    ReflexiveCoupleTypes = 1037
    RemoteSuperSubTypes = 1038
    RemoteTypesInstances = 1039
    RemoteWholesParts = 1040
    Representations = 1041
    RepresentedBy = 1042
    Signs = 1043
    Singletons = 1044
    StrictSuperSubTypes = 1045
    StrictWholesParts = 1046
    SymmetricCoupleTypes = 1047
    TemporalStages = 1048
    TransitiveCoupleTypes = 1049
    Triples = 1050
    VariableArityTupleTypes = 1051

    BoroCoreIdentifiers = 1052

    # endregion  // Ontology

    # region Agentology

    DefaultNfMentionFormulaNames = 2001
    DefaultObjectSignStoreFormulaNames = (
        2002
    )
    ObjectSignRepositoryIndices = 2003
    ThisNfAgent = 2004
    TnfaCommonReservedNames = 2005
    TnfaEarCommonReservedNames = 2006
    TnfaExemplarTypesInstances = 2007
    TnfaRootNamingSpaceNames = 2008

    # endregion  // Agentology


def get_immutable_tuple_infrastructure_subtype_ck_ids():
    immutable_tuple_infrastructure_subtype_ck_ids = {
        BoroObjectCkIds.Tuples,
        BoroObjectCkIds.SuperSubTypes,
        BoroObjectCkIds.WholesParts,
        BoroObjectCkIds.TypesInstances,
        BoroObjectCkIds.PowerTypesInstances,
        BoroObjectCkIds.NamedBy,
        BoroObjectCkIds.RepresentedBy,
    }

    return immutable_tuple_infrastructure_subtype_ck_ids


def get_composition_couple_types_ck_ids():
    composition_couple_types_ck_ids = {
        BoroObjectCkIds.SuperSubTypes,
        BoroObjectCkIds.WholesParts,
        BoroObjectCkIds.TypesInstances,
        BoroObjectCkIds.PowerTypesInstances,
    }

    return (
        composition_couple_types_ck_ids
    )


def is_immutable_tuple_infrastructure_subtype_reflexive(
    boroObjectCkId,
):
    if (
        boroObjectCkId
        == BoroObjectCkIds.SuperSubTypes
    ):
        return True

    if (
        boroObjectCkId
        == BoroObjectCkIds.WholesParts
    ):
        return True

    return False
