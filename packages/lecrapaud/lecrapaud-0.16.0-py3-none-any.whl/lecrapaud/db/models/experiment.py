from itertools import chain
import joblib

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    JSON,
    Table,
    ForeignKey,
    BigInteger,
    TIMESTAMP,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship, aliased
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from statistics import fmean as mean
from lecrapaud.db.models.model_selection import ModelSelection
from lecrapaud.db.models.model_training import ModelTraining
from lecrapaud.db.models.score import Score

from lecrapaud.db.models.base import Base, with_db
from lecrapaud.db.models.utils import create_association_table

# jointures
lecrapaud_experiment_target_association = create_association_table(
    name="experiment_target_association",
    table1="experiments",
    column1="experiment",
    table2="targets",
    column2="target",
)


class Experiment(Base):

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    name = Column(String(50), nullable=False)
    path = Column(String(255))  # we do not have this at creation time
    type = Column(String(50), nullable=False)
    size = Column(Integer, nullable=False)
    train_size = Column(Integer)
    val_size = Column(Integer)

    # Relationships
    model_selections = relationship(
        "ModelSelection",
        back_populates="experiment",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @hybrid_property
    def best_rmse(self):
        """Best RMSE score across all model selections and trainings."""
        # Get the minimum RMSE for each model selection
        min_scores = [
            min(
                score.rmse
                for mt in ms.model_trainings
                for score in mt.score
                if score.rmse is not None
            )
            for ms in self.model_selections
            if any(
                score.rmse is not None
                for mt in ms.model_trainings
                for score in mt.score
            )
        ]
        return min(min_scores) if min_scores else None

    @hybrid_property
    def best_logloss(self):
        """Best LogLoss score across all model selections and trainings."""
        # Get the minimum LogLoss for each model selection
        min_scores = [
            min(
                score.logloss
                for mt in ms.model_trainings
                for score in mt.score
                if score.logloss is not None
            )
            for ms in self.model_selections
            if any(
                score.logloss is not None
                for mt in ms.model_trainings
                for score in mt.score
            )
        ]
        return min(min_scores) if min_scores else None

    @hybrid_property
    def avg_rmse(self):
        """Average RMSE score across all model selections and trainings."""
        # Get the minimum RMSE for each model selection
        min_scores = [
            min(
                score.rmse
                for mt in ms.model_trainings
                for score in mt.score
                if score.rmse is not None
            )
            for ms in self.model_selections
            if any(
                score.rmse is not None
                for mt in ms.model_trainings
                for score in mt.score
            )
        ]
        return mean(min_scores) if min_scores else None

    @hybrid_property
    def avg_logloss(self):
        """Average LogLoss score across all model selections and trainings."""
        # Get the minimum LogLoss for each model selection
        min_scores = [
            min(
                score.logloss
                for mt in ms.model_trainings
                for score in mt.score
                if score.logloss is not None
            )
            for ms in self.model_selections
            if any(
                score.logloss is not None
                for mt in ms.model_trainings
                for score in mt.score
            )
        ]
        return mean(min_scores) if min_scores else None

    test_size = Column(Integer)
    corr_threshold = Column(Float, nullable=False)
    max_features = Column(Integer, nullable=False)
    percentile = Column(Float, nullable=False)
    number_of_groups = Column(Integer)
    list_of_groups = Column(JSON)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    train_start_date = Column(DateTime)
    train_end_date = Column(DateTime)
    val_start_date = Column(DateTime)
    val_end_date = Column(DateTime)
    test_start_date = Column(DateTime)
    test_end_date = Column(DateTime)
    context = Column(JSON)

    feature_selections = relationship(
        "FeatureSelection",
        back_populates="experiment",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    targets = relationship(
        "Target",
        secondary=lecrapaud_experiment_target_association,
        back_populates="experiments",
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            name="uq_experiments_composite",
        ),
    )

    @classmethod
    @with_db
    def get_all_by_name(cls, name: str | None = None, db=None):
        """
        Find the most recently created experiment that contains the given name string.

        Args:
            session: SQLAlchemy session
            name (str): String to search for in experiment names

        Returns:
            Experiment or None: The most recent matching experiment or None if not found
        """
        if name is not None:
            return (
                db.query(cls)
                .filter(cls.name.ilike(f"%{name}%"))
                .order_by(cls.created_at.desc())
                .all()
            )
        return db.query(cls).order_by(cls.created_at.desc()).all()

    @classmethod
    @with_db
    def get_last_by_name(cls, name: str, db=None):
        """
        Find the most recently created experiment that contains the given name string.

        Args:
            session: SQLAlchemy session
            name (str): String to search for in experiment names

        Returns:
            Experiment or None: The most recent matching experiment or None if not found
        """
        return (
            db.query(cls)
            .filter(cls.name.ilike(f"%{name}%"))
            .order_by(cls.created_at.desc())
            .first()
        )

    @classmethod
    @with_db
    def get_best_by_score(cls, name: str, metric="both", db=None):
        """
        Find the experiment with the best score based on average RMSE, LogLoss, or both.

        Args:
            metric (str): 'rmse', 'logloss', or 'both' to determine which score to optimize
            db: SQLAlchemy session

        Returns:
            Experiment or None: The experiment with the best score or None if not found
        """
        if metric == "both":
            # Calculate a combined score: average of normalized RMSE and LogLoss
            # This ensures we're comparing apples to apples by normalizing the scores
            experiments = db.query(cls).filter(cls.name.ilike(f"%{name}%")).all()
            if not experiments:
                return None

            # Get all scores
            rmse_scores = [e.avg_rmse for e in experiments if e.avg_rmse is not None]
            logloss_scores = [
                e.avg_logloss for e in experiments if e.avg_logloss is not None
            ]

            if not rmse_scores or not logloss_scores:
                return None

            # Normalize scores (subtract min and divide by range)
            min_rmse = min(rmse_scores)
            range_rmse = max(rmse_scores) - min_rmse
            min_logloss = min(logloss_scores)
            range_logloss = max(logloss_scores) - min_logloss

            # Calculate combined score for each experiment
            experiment_scores = []
            for experiment in experiments:
                if experiment.avg_rmse is None or experiment.avg_logloss is None:
                    continue

                # Normalize both scores
                norm_rmse = (experiment.avg_rmse - min_rmse) / range_rmse
                norm_logloss = (experiment.avg_logloss - min_logloss) / range_logloss

                # Calculate combined score (average of normalized scores)
                combined_score = (norm_rmse + norm_logloss) / 2
                experiment_scores.append((experiment, combined_score))

            # Sort by combined score (ascending since lower is better)
            experiment_scores.sort(key=lambda x: x[1])

            return experiment_scores[0][0] if experiment_scores else None

        # For single metric case (rmse or logloss)
        score_property = cls.avg_rmse if metric == "rmse" else cls.avg_logloss

        return (
            db.query(cls)
            .filter(
                cls.name.ilike(f"%{name}%"), score_property.isnot(None)
            )  # Only consider experiments with scores
            .order_by(score_property)
            .first()
        )

    def get_features(self, target_number: int):
        targets = [t for t in self.targets if t.name == f"TARGET_{target_number}"]
        if targets:
            target_id = targets[0].id
            feature_selection = [
                fs for fs in self.feature_selections if fs.target_id == target_id
            ]
            if feature_selection:
                feature_selection = feature_selection[0]
                features = [f.name for f in feature_selection.features]
                return features

        # fallback to path if no features found
        features = joblib.load(f"{self.path}/TARGET_{target_number}/features.pkl")
        return features

    def get_all_features(self, date_column: str = None, group_column: str = None):
        target_idx = [target.id for target in self.targets]
        _all_features = chain.from_iterable(
            [f.name for f in fs.features]
            for fs in self.feature_selections
            if fs.target_id in target_idx
        )
        _all_features = list(_all_features)

        # fallback to path if no features found
        if len(_all_features) == 0:
            _all_features = joblib.load(f"{self.path}/preprocessing/all_features.pkl")

        all_features = []
        if date_column:
            all_features.append(date_column)
        if group_column:
            all_features.append(group_column)
        all_features += _all_features
        all_features = list(dict.fromkeys(all_features))

        return all_features
